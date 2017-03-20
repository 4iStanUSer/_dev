import os
import re
import pandas as pd
import logging


def collects_data(config):
    """"
        Collect data from external storage into DataFrame
    """
    format = config['format']
    if format in ['csv', 'txt']:
        return collect_data(config)
    elif format == 'excel':
        return collect_data_xls(config)
    elif format == 'hdf':
        collect_from_hdf(config)
    else:
        pass


def collect_from_hdf(config):
    """
    Read from hdf storage and get Dataframe
    """
    try:
        storage_path = config['storage_path']
        table_name = config['table_name']
    except KeyError:
        logging.info("Wrong Input File")
        raise Exception
    else:
        columns = config['columns']
        chunk_size = config['chunk_size']
        format = config['format']
        where = config['where']
    if format == 'hdf':
        with pd.HDFStore(storage_path) as store:
             for chunk in store.select(table_name, columns=columns,
                                       auto_close=True, where=where,
                                       chunksize=chunk_size):
                logging.info(
                "Data Collected - storage_path: {0} - Table {1} - Chunk {2}".
                              format(storage_path, table_name, chunk_size))
                yield chunk
    else:
        return None


def preprocess(file, col_to_read, columns, sep):

    try:
        row = pd.read_table(file, sep=sep, nrows=1)
        if set(columns) >= set(col_to_read) and \
            len(columns) == len(row.columns):
            return True
        else:
            x = len(columns) == len(row.columns)
            return False
    except Exception:
        return False


def collect_data(config):
    """"
    Collect data from external storage into DataFrame
    """


    try:
        data_path = config['data_folder']
        filename_mask = config['file_mask']
    except KeyError:
        logging.info("wrong input file")
        raise Exception


    columns = config['columns'].split(',')
    try:
        chunk_size = int(config['chunk_size'])
    except ValueError:
        chunk_size = None
    sep = config['sep']
    header = config['header']

    try:
        cols_props = config['columns_properties']
        col_to_read = [i['col_name'] for i in cols_props]
    except KeyError:
        index_cols = None
        col_to_read = columns
    else:
        index_cols = [ind for ind, x in enumerate(cols_props)
                      if x['col_type'] == 'index']
        if index_cols==[]:
            index_cols = None
    filenames = scan_folder(data_path, filename_mask)

    for file in filenames:

        preprocess_result = preprocess(file, col_to_read=col_to_read,
                                       columns=columns, sep=sep)

        if header and preprocess_result:
            for chunk in pd.read_table(file, header=0, usecols=col_to_read,
                                       chunksize=chunk_size, sep=sep,
                                       iterator=True):

                logging.info("Data Collected - File: {0} - Chunk {1}".
                             format(file, chunk_size))
                yield chunk

        elif preprocess_result and not header:
            for chunk in pd.read_table(file, header=None, usecols=col_to_read,
                                       names=columns, chunksize=chunk_size,
                                       sep=sep, index_col=index_cols,
                                       iterator=True):

                logging.info("Data Collected - File {0} - Chunk {1}".
                             format(file, chunk_size))
                yield chunk
        else:
            logging.info("No valid format of input columns - {0}".format(file))
            raise Exception


def collect_data_xls(config):
    """"
    Collect data from external xls storage into DataFrame
    """
    try:
        data_path = config['data_folder']
        filename_mask = config['file_mask']
    except KeyError:
        logging.info("Wrong Input File")
        raise Exception

    columns = config['columns'].split(",")
    format = config['format']
    sep = config['sep']
    filenames = scan_folder(data_path, filename_mask)

    for path in filenames:
        if format == 'xls':
            xls = pd.ExcelFile(path)
            df = xls.parse(header=0, sep=sep, usecols=columns)
            logging.info("Data Collected - {0}".format(path))
            yield df


def collect_to_hdf(config, processor):
    """
    Reading from .csv file and saving to hdf
    """
    try:
        table_name = config['table_name']
        storage_path = config['storage']
        mode = config['mode']
    except KeyError:
        logging.info("wrong input file-{0}-{1}".
                     format(table_name, storage_path))
        raise Exception
    cols_props = config['columns_properties']
    data_cols = [x['col_name'] for x in cols_props if x['is_index_data_col']]

    with pd.HDFStore(storage_path, mode='a') as store:
        if mode == 'w' and table_name in store.keys():
            store.remove(table_name)
        for df in collects_data(config):
            if processor:
                result = processor(df)
                result = process_types(result, cols_props)
            else:
                result = process_types(df, cols_props)


            result.to_hdf(storage_path, table_name, append=True,
                          format='t',
                          min_itemsize=100)
            logging.info("Stored to Hdf: Storage - {0} Table - {1}"
                         .format(storage_path, table_name))
        store.create_table_index(table_name, columns=data_cols, kind='full')


def scan_folder(path, mask):
    f_names = []
    compiled_mask = re.compile(mask)
    for filename in os.listdir(path):
        match_res = compiled_mask.match(filename)
        if not match_res:
            continue
        f_names.append(os.path.join(path, filename))
    return f_names


def process_types(df, cols_props):
    for col_item in cols_props:
        c_name = col_item['col_name']
        if col_item['col_type'] == 'numeric':

            df[c_name] = pd.to_numeric(df[c_name], errors='coerce')\
                .astype('float64')
        elif col_item['col_type'] == 'categorical':

            df[c_name] = df[c_name]\
                .astype('category', categories=col_item['options'])
        elif col_item['col_type'] == 'date':

            df[c_name] = \
                pd.to_datetime(df[c_name], format=col_item['format'],
                               errors='coerce')
        elif col_item['col_type'] == 'object':

            df[c_name] = df[c_name].astype('object')
    return df


def out_process_data_var_col(df, variables, time_stamp_column):
    """
    Process data into output format - Variable: var_1, var_ var_3
                                      TimeStamp_1: 2, 203, 13
                                      TimeStamp_2: 0, 12, 20
    """

    time_stamps = list(df[time_stamp_column].unique())
    for var in variables:
        for time_stamp in time_stamps:
            col_name = var + "_" + str(time_stamp)
            df[col_name] = None
            df[col_name][(df[time_stamp_column] == time_stamp)] = \
                df[var][(df[time_stamp_column] == time_stamp)].\
                    apply(lambda x: x)
        del df[var]
        df.drop_duplicates()
    return df


def out_process_data_var_ts_col(df, variables, time_stamp_column):
    """
    Output processing into format Time_Stamp_1_Var: 1,1,2
                                  Time_Stamp_2_Var: 1,2,3

    Inputs:
        config
        DataFrame
    Output:
        Change format of DataFrame
    """

    time_stamps = list(df[time_stamp_column].unique())

    frames = []
    for var_name in variables:
        df["variable"] = var_name
        for time_stamp in time_stamps:
            df[time_stamp] = None
            df[time_stamp][(df['variable'] == var_name)] = \
                df[(df[time_stamp_column] == time_stamp)][var_name].\
                    apply(lambda x: x)

        df.drop_duplicates()
        frames.append(df)

    for var_name in vars:
        del df[var_name]
    df = pd.concat(frames)
    return df


def write(df, path, format, sep=',', mode='w'):
    """
    Save to external storage Csv or XLS
    """
    if format == 'csv':
        df.to_csv(path+'.csv', sep=sep, mode=mode)

    elif format == 'xls':
        df.to_excel(path, sep=sep, mode=mode)

    logging.info("File is writen: {0}".format(path))




