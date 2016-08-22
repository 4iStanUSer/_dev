from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col, \
    get_cell_range, mapping
# from iap.repository.tmp_db_interface import *
import collections
import datetime


def jj_oral_care_rgm_sales(warehouse, wb, options_list):
    t1 = datetime.datetime.now()

    ws = wb.sheet_by_index(0)
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row_index = options_list['info']['header_row']
    name_col = options_list['name_col']
    if 'map_names' in options_list:
        has_map_names = True
        map_names = options_list['map_names']
    else:
        has_map_names = False
    series_name = options_list['dates_info']['scale']
    start_data_row = options_list['info']['data_row']
    start_date_col = options_list['dates_info']['start_column']
    last_col = options_list['dates_info']['end_column']
    if last_col == '':
        last_col = get_last_col(data, header_row_index)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = data[header_row_index][key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    # Data processing
    date_values = []
    date_rows = options_list['dates_info']['dates_rows']
    for row_index in date_rows:
        date_values.append(data[row_index][start_date_col].value)
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(date_values, num_of_dates)
    times_series = warehouse.add_time_scale(series_name, time_line)
    for row_index in range(start_data_row, len(data)):
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
        # Using db interface
        var_name = data[row_index][name_col].value
        if has_map_names:
            if var_name in map_names:
                var_name = map_names[var_name]
        entity = warehouse.add_entity(meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(times_series)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data[row_index][col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)
    t2 = datetime.datetime.now()
    delta = (t2 - t1)
    minutes_delta_time = delta.seconds / 60.0
    print('Algorithm rgm sales takes minutes:' + str(minutes_delta_time))
    print('Algorithm rgm sales takes seconds:' + str(delta.seconds))


def jj_oral_care_media_spend(warehouse, wb, options_list):
    t1 = datetime.datetime.now()

    ws = wb.sheet_by_index(0)
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row_index = options_list['info']['header_row']
    name_col = options_list['name_col']
    if 'map_names' in options_list:
        has_map_names = True
        map_names = options_list['map_names']
    else:
        has_map_names = False
    series_name = options_list['dates_info']['scale']
    start_data_row = options_list['info']['data_row']
    start_date_col = options_list['dates_info']['start_column']
    last_col = options_list['dates_info']['end_column']
    if last_col == '':
        last_col = get_last_col(data, header_row_index)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = data[header_row_index][key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    # Data processing
    date_values = []
    date_rows = options_list['dates_info']['dates_rows']
    for row_index in date_rows:
        date_values.append(data[row_index][start_date_col].value)
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(date_values, num_of_dates)
    times_series = warehouse.add_time_scale(series_name, time_line)
    for row_index in range(start_data_row, len(data)):
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
        # Using db interface
        var_name = data[row_index][name_col].value
        if has_map_names:
            if var_name in map_names:
                var_name = map_names[var_name]
        entity = warehouse.add_entity(meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(times_series)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data[row_index][col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)
    t2 = datetime.datetime.now()
    delta = (t2 - t1)
    minutes_delta_time = delta.seconds / 60.0
    print('Algorithm media spend takes minutes:' + str(minutes_delta_time))
    print('Algorithm media spend takes seconds:' + str(delta.seconds))


def jj_oral_care_sku(warehouse, wb, options_list):
    t1 = datetime.datetime.now()

    ws = wb.sheet_by_index(0)
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row_index = options_list['info']['header_row']
    name_col = options_list['name_col']
    map_names = options_list['map_names']
    series_name = options_list['dates_info']['scale']
    start_data_row = options_list['info']['data_row']
    start_date_col = options_list['dates_info']['start_column']
    last_col = options_list['dates_info']['end_column']
    if last_col == '':
        last_col = get_last_col(data, header_row_index)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = data[header_row_index][key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(
        data[header_row_index][start_date_col].value, wb.datemode,
        num_of_dates)
    times_series = warehouse.add_time_scale(series_name, time_line)
    for row_index in range(start_data_row, len(data)):
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
        # Using db interface
        var_name = data[row_index][name_col].value
        if var_name in map_names:
            var_name = map_names[var_name]
        entity = warehouse.add_entity(meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(times_series)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data[row_index][col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)
    t2 = datetime.datetime.now()
    delta = (t2 - t1)
    minutes_delta_time = delta.seconds / 60.0
    print('Algorithm sku takes minutes:' + str(minutes_delta_time))
    print('Algorithm sku takes seconds:' + str(delta.seconds))
