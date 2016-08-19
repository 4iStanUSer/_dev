from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col, \
    get_cell_range, mapping
import collections
from iap.data_processing.processors.jj_aggr_map import DataAggregate
import datetime


def jj_brand_extract_speed_test(warehouse, wb, options_list):
    meta_cols = options_list['meta_cols']
    data_cols = options_list['data_cols']
    dates_src_cols = options_list['dates_cols']
    date_func = options_list['data_func']
    date_col = options_list['dates_cols']['date_col']
    series_name = options_list['dates_cols']['scale']
    ws = wb.sheet_by_index(0)
    if ws.nrows <= 1:
        raise ex.EmptyInputsError('jj_extract')
    header_row = ws.row(0)
    last_col = get_last_col(ws, header_row)
    # Init headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value
    for key, val in data_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            data_cols[key] = header_row[key].value
    if date_col >= last_col:
        raise ex.NotExistsError('DataProcessing', 'column', key)
    # Create output: Append data
    output = []
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    date_values = []
    for row_index in range(1, ws.nrows):
        date_values.append(data[row_index][date_col].value)
    time_line = get_time_line(date_values)
    warehouse.add_time_scale(series_name, time_line)
    warehouse.commit()
    for row_index in range(1, ws.nrows):
        # if row_index == 1 or row_index == 63:
        print(row_index)
        meta = []
        meta_dict = collections.OrderedDict({})
        for key, val in meta_cols.items():
            meta_dict[val] = data[row_index][key].value
            meta.append(data[row_index][key].value)
        if mapping_rule is not None:
            new_meta_dict = mapping(meta_dict, mapping_rule)
            meta = []
            for key, value in new_meta_dict.items():
                meta.append(value)
        num_of_dates = 1
        date_value = data[row_index][date_col].value
        start_label = date_func(date_value, num_of_dates)
        # IWarehouse.add_time_scale(ssn, series_name, time_line)
        entity = warehouse.add_entity(meta)
        for key, val in data_cols.items():
            value = data[row_index][key].value
            variable = entity.force_variable(val, 'float')
            time_series = variable.force_time_series(series_name)
            history_value = time_series.get_value(start_label)
            if not history_value:
                new_value = [value]
            else:
                new_value = [history_value[0] + value]
            time_series.set_values(start_label, new_value)
    return output


def jj_brand_extract(warehouse, wb, options_list):
    t1 = datetime.now()

    meta_cols = options_list['meta_cols']
    data_cols = options_list['data_cols']
    dates_src_cols = options_list['dates_cols']
    date_func = options_list['data_func']
    date_col = options_list['dates_cols']['date_col']
    series_name = options_list['dates_cols']['scale']
    ws = wb.sheet_by_index(0)
    if ws.nrows <= 1:
        raise ex.EmptyInputsError('jj_extract')
    header_row = ws.row(0)
    last_col = get_last_col(ws, header_row)
    # Init headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value
    for key, val in data_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            data_cols[key] = header_row[key].value
    if date_col >= last_col:
        raise ex.NotExistsError('DataProcessing', 'column', key)
    # Create output: Append data
    output = []
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    date_values = []
    for row_index in range(1, ws.nrows):
        date_values.append(data[row_index][date_col].value)
    time_line = get_time_line(date_values)
    warehouse.add_time_scale(series_name, time_line)
    warehouse.commit()
    for row_index in range(1, ws.nrows):
        # if row_index == 1 or row_index == 63:
        print(row_index)
        meta = []
        meta_dict = collections.OrderedDict({})
        for key, val in meta_cols.items():
            meta_dict[val] = data[row_index][key].value
            meta.append(data[row_index][key].value)
        if mapping_rule is not None:
            new_meta_dict = mapping(meta_dict, mapping_rule)
            meta = []
            for key, value in new_meta_dict.items():
                meta.append(value)
        num_of_dates = 1
        date_value = data[row_index][date_col].value
        start_label = date_func(date_value, num_of_dates)
        # IWarehouse.add_time_scale(ssn, series_name, time_line)
        entity = warehouse.add_entity(meta)
        for key, val in data_cols.items():
            value = data[row_index][key].value
            variable = entity.force_variable(val, 'float')
            time_series = variable.force_time_series(series_name)
            history_value = time_series.get_value(start_label)
            if not history_value:
                new_value = [value]
            else:
                new_value = [history_value[0] + value]
            time_series.set_values(start_label, new_value)
        if row_index == 134:
            t3 = datetime.now()
            delta = (t3 - t1)
            minutes_delta_time = delta.seconds/60.0
            print('Algorithm 134 takes minutes:' + str(minutes_delta_time))
            print('Algorithm 143 takes seconds:' + str(delta.seconds))
    t2 = datetime.now()
    delta = (t2 - t1)
    minutes_delta_time = delta.seconds/60.0
    print('Algorithm takes minutes:' + str(minutes_delta_time))
    print('Algorithm takes seconds:' + str(delta.seconds))
    return output


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
    meta_new_names = options_list['meta_cols']
    name_col_num = options_list['name_col']
    dates_info = options_list['dates_cols']

    ws = wb.sheet_by_name('Report1')
    # Initialize data start
    data_header_row_index = 0
    start_meta_row = 0
    for row_index in range(ws.nrows):
        desc_val = str(ws.cell(row_index, name_col_num).value)
        # if  isinstance(curr_val, str):
        desc_val = desc_val.strip().lower()
        if desc_val == 'description':
            data_header_row_index = row_index
            start_meta_row = row_index + 2
            break
    if data_header_row_index == 0:
        raise ex.EmptyInputsError('data')
    # Assign header_row(dates header) and last column(not higher then ws.ncols)
    header_row = ws.row(data_header_row_index)
    start_dates_col = dates_info['start_column']
    end_dates_col = dates_info['end_column']
    if end_dates_col == '':
        end_dates_col = get_last_col(ws, header_row)
    # Initialize data: meta table and data table
    row_index = data_header_row_index+1
    meta_column = ws.col(name_col_num)
    num_of_dates = end_dates_col - start_dates_col
    first_label, time_line = date_func(header_row[start_dates_col].value,
                                       num_of_dates)
    # start_date_point = date_func(header_row[start_dates_col].value)
    series_name = dates_info['scale']
    warehouse.add_time_scale(series_name, time_line)
    while row_index < ws.nrows:
        desc_val = str(meta_column[row_index].value)
        # Add meta and data to output only if facts exist
        if desc_val.strip().lower() == 'facts':
            last_meta_row = row_index - 1
            last_facts_row = __get_last_facts_row(ws, row_index+1, ws.nrows,
                                                  end_dates_col)
            # Looking for facts by rows and data by columns, add data to db
            # using db interface
            meta = __get_meta(meta_column, meta_new_names, start_meta_row,
                              last_meta_row)
            entity = warehouse.add_entity(meta)
            for row_index in range(row_index+1, last_facts_row + 1):
                data_row = ws.row(row_index)
                fact_name = meta_column[row_index].value
                variable = entity.force_variable(fact_name, 'float')
                values = []
                for col_index in range(start_dates_col, end_dates_col):
                    values.append(data_row[col_index].value)
                time_series = variable.force_time_series(series_name)
                time_series.set_values(first_label, values)
            row_index = last_facts_row
            start_meta_row = last_facts_row + 1
        row_index += 1


def __get_meta(meta_column, meta_new_names, start_meta_row, last_meta_row):
    meta = []
    index = 0
    for row_index in range(start_meta_row, last_meta_row + 1):
        if meta_new_names[index] == '':
            desc_val = str(meta_column[row_index].value)
        else:
            desc_val = meta_new_names[index]
        meta.append(desc_val)
        index += 1
    return meta


def __get_last_facts_row(ws, start_facts_row, last_row, last_col):
    last_facts_row = 0
    for row_index in range(start_facts_row, last_row):
        data_row = ws.row(row_index)
        if data_row[1].ctype == 0:
            is_total = True
            for col_index in range(1,last_col):
                if data_row[col_index].ctype != 0:
                    is_total = False
                    break
            if is_total:
                last_facts_row = row_index - 1
                break
    if last_facts_row == 0:
        last_facts_row = last_row - 1
    return last_facts_row
