from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col, \
    get_cell_range, mapping
import collections
import datetime


def jj_brand_extract(warehouse, wb, options_list):
    # t1 = datetime.datetime.now()

    meta_cols = options_list['meta_cols']
    data_cols = options_list['data_cols']
    dates_info = options_list['dates_cols']
    date_func = options_list['data_func']
    date_col = dates_info['date_col']
    series_name = dates_info['scale']
    ws = wb.sheet_by_index(0)
    if ws.nrows <= 1:
        raise ex.EmptyInputsError('jj_extract')
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    header_row_index = 0
    last_col = get_last_col(data, header_row_index)
    # Init headers cols: names
    for item in meta_cols:
        column_number = item['Col_number']
        if column_number >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', column_number)
        if item['Dimension_name'] == '':
            item['Dimension_name'] = data[0][column_number].value
    for key, val in data_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            data_cols[key] = data[0][key].value
    if date_col >= last_col:
        raise ex.NotExistsError('DataProcessing', 'column', key)
    # Create output: Append data
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    date_values = []
    for row_index in range(1, len(data)):
        date_values.append(data[row_index][date_col].value)
    time_line = get_time_line(date_values)
    times_series = warehouse.add_time_scale(series_name, time_line)
    for row_index in range(1, len(data)):
        # print(row_index)
        meta = []
        for item in meta_cols:
            copy_item = item.copy()
            column_index = copy_item['Col_number']
            copy_item['Name'] = data[row_index][column_index].value
            meta.append(copy_item)
        if mapping_rule is not None:
            new_meta, is_mapped = mapping(meta, mapping_rule)
            if is_mapped:
                meta = new_meta
        num_of_dates = 1
        date_value = data[row_index][date_col].value
        start_label = date_func(date_value, num_of_dates)
        entity = warehouse.add_entity(meta)
        for key, val in data_cols.items():
            value = data[row_index][key].value
            variable = entity.force_variable(val, 'float')
            time_series = variable.force_time_series(times_series)
            history_value = time_series.get_value(start_label)
            if not history_value:
                new_value = [value]
            else:
                new_value = [history_value + value]
            time_series.set_values(start_label, new_value)
    # t2 = datetime.datetime.now()
    # delta = (t2 - t1)
    # minutes_delta_time = delta.seconds/60.0
    # print('Algorithm takes minutes:' + str(minutes_delta_time))
    # print('Algorithm takes seconds:' + str(delta.seconds))


def get_time_line(date_values):
    output = collections.OrderedDict({})
    min_val = min(date_values)
    max_val = max(date_values)
    # Init max min dates
    min_year = int(str(min_val)[0:4])
    min_week = int(str(min_val)[4:6])
    max_year = int(str(max_val)[0:4])
    max_week = int(str(max_val)[4:6])
    # Create output
    start_date = str(int(min_val))
    time_stamp = datetime.datetime.strptime(start_date + '-0', "%Y%W-%w")
    diff_years = max_year - min_year
    num_of_dates = (52 - min_week + 1) + diff_years*52 - (52 - max_week)
    week = min_week
    year = min_year
    for i in range(num_of_dates):
        if week > 52:
            year += 1
            week -= 52
        new_key = str(year) + ' W' + str(week)
        output[new_key] = time_stamp
        week += 1
        time_stamp += datetime.timedelta(days=7)
    return output


def jj_brand(warehouse, wb, options_list):
    date_func = options_list['date_func']
    meta_cols = options_list['meta_cols']
    name_col_num = options_list['name_col']
    dates_info = options_list['dates_cols']

    ws = wb.sheet_by_name('Report1')
    # Initialize data start
    data_header_row_index = 0
    start_meta_row = 0
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    for row_index in range(len(data)):
        desc_val = str(data[row_index][name_col_num].value)
        # if  isinstance(curr_val, str):
        desc_val = desc_val.strip().lower()
        if desc_val == 'description':
            data_header_row_index = row_index
            start_meta_row = row_index + 2
            break
    if data_header_row_index == 0:
        raise ex.EmptyInputsError('data')
    # Assign header_row(dates header) and last column(not higher then ws.ncols)
    start_dates_col = dates_info['start_column']
    end_dates_col = dates_info['end_column']
    if end_dates_col == '':
        end_dates_col = get_last_col(data, data_header_row_index)
    # Initialize data: meta table and data table
    row_index = data_header_row_index+1
    num_of_dates = end_dates_col - start_dates_col
    first_label, time_line = date_func(
        data[data_header_row_index][start_dates_col].value, num_of_dates)
    # start_date_point = date_func(header_row[start_dates_col].value)
    series_name = dates_info['scale']
    times_series = warehouse.add_time_scale(series_name, time_line)
    full_meta = []
    while row_index < len(data):
        desc_val = str(data[row_index][name_col_num].value)
        # Add meta and data to output only if facts exist
        if desc_val.strip().lower() == 'facts':
            last_meta_row = row_index - 1
            last_facts_row = __get_last_facts_row(data, row_index+1, len(data),
                                                  end_dates_col)
            # Looking for facts by rows and data by columns, add data to db
            # using db interface
            # collecting meta
            meta = __get_meta(data, name_col_num, meta_cols,
                              start_meta_row,
                              last_meta_row)
            len_meta = len(meta)
            if not full_meta:
                for item in meta:
                    full_meta.append(item.copy())
            elif len_meta > len(full_meta):
                # TODO Exception
                raise Exception
            elif len_meta <= len(full_meta):
                for i in range(len_meta):
                    full_meta[-len_meta+i] = meta[i].copy()
                meta = full_meta
            # working with WH interface
            entity = warehouse.add_entity(meta)
            for row_index in range(row_index+1, last_facts_row + 1):
                fact_name = data[row_index][name_col_num].value
                variable = entity.force_variable(fact_name, 'float')
                values = []
                for col_index in range(start_dates_col, end_dates_col):
                    values.append(data[row_index][col_index].value)
                time_series = variable.force_time_series(times_series)
                time_series.set_values(first_label, values)
            row_index = last_facts_row
            start_meta_row = last_facts_row + 1
        row_index += 1


def __get_meta(data, meta_column, meta_cols, start_meta_row,
               last_meta_row):
    meta = []
    name_desc = 'Name'
    index = 0
    reverse_index = (last_meta_row - start_meta_row) + 1
    for row_index in range(start_meta_row, last_meta_row + 1):
        new_dict = meta_cols[-reverse_index].copy()
        if meta_cols[index][name_desc] == '':
            desc_val = str(data[row_index][meta_column].value)
        else:
            desc_val = meta_cols[index][name_desc]
        new_dict[name_desc] = desc_val
        meta.append(new_dict)
        index += 1
        reverse_index -= 1
    return meta


def __get_last_facts_row(data, start_facts_row, last_row, last_col):
    last_facts_row = 0
    for row_index in range(start_facts_row, last_row):
        if data[row_index][1].ctype == 0:
            is_total = True
            for col_index in range(1, last_col):
                if data[row_index][col_index].ctype != 0:
                    is_total = False
                    break
            if is_total:
                last_facts_row = row_index - 1
                break
    if last_facts_row == 0:
        last_facts_row = last_row - 1
    return last_facts_row
