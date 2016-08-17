from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col, \
    get_cell_range, mapping
from iap.repository.interface.iwarehouse import IWarehouse
# from iap.repository.tmp_db_interface import *
import collections


def jj_oral_care_rgm_sales(ssn, wb, options_list):
    ws = wb.sheet_by_index(0)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row = ws.row(options_list['info']['header_row'])
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
        last_col = get_last_col(ws, header_row)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    # Data processing
    date_values = []
    date_rows = options_list['dates_info']['dates_rows']
    for row_index in date_rows:
        date_values.append(ws.cell(row_index, start_date_col).value)
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(date_values, num_of_dates)
    IWarehouse.add_time_scale(ssn, series_name, time_line)
    counter = 0
    for row_index in range(start_data_row, ws.nrows):
        counter += 1
        data_row = ws.row(row_index)
        meta = []
        meta_dict = collections.OrderedDict({})
        for key, val in meta_cols.items():
            meta_dict[val] = data_row[key].value
            meta.append(data_row[key].value)
        if mapping_rule is not None:
            new_meta_dict = mapping(meta_dict, mapping_rule)
            meta = []
            for key, value in new_meta_dict.items():
                meta.append(value)
        # Using db interface
        var_name = data_row[name_col].value
        if has_map_names:
            if var_name in map_names:
                var_name = map_names[var_name]
        entity = IWarehouse.add_entity(ssn, meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(series_name)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data_row[col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)


def jj_oral_care_media_spend(ssn, wb, options_list):
    ws = wb.sheet_by_index(0)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row = ws.row(options_list['info']['header_row'])
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
        last_col = get_last_col(ws, header_row)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    # Data processing
    date_values = []
    date_rows = options_list['dates_info']['dates_rows']
    for row_index in date_rows:
        date_values.append(ws.cell(row_index, start_date_col).value)
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(date_values, num_of_dates)
    IWarehouse.add_time_scale(ssn, series_name, time_line)
    for row_index in range(start_data_row, ws.nrows):
        data_row = ws.row(row_index)
        meta = []
        meta_dict = collections.OrderedDict({})
        for key, val in meta_cols.items():
            meta_dict[val] = data_row[key].value
            meta.append(data_row[key].value)
        if mapping_rule is not None:
            new_meta_dict = mapping(meta_dict, mapping_rule)
            meta = []
            for key, value in new_meta_dict.items():
                meta.append(value)
        # Using db interface
        var_name = data_row[name_col].value
        if has_map_names:
            if var_name in map_names:
                var_name = map_names[var_name]
        entity = IWarehouse.add_entity(ssn, meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(series_name)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data_row[col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)


def jj_oral_care_sku(ssn, wb, options_list):
    ws = wb.sheet_by_index(0)
    meta_cols = options_list['meta_cols']
    date_func = options_list['date_func']
    header_row = ws.row(options_list['info']['header_row'])
    name_col = options_list['name_col']
    map_names = options_list['map_names']
    series_name = options_list['dates_info']['scale']
    start_data_row = options_list['info']['data_row']
    start_date_col = options_list['dates_info']['start_column']
    last_col = options_list['dates_info']['end_column']
    if last_col == '':
        last_col = get_last_col(ws, header_row)
    # Rename headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value
    # Data processing
    if 'mapping_rule' in options_list:
        mapping_rule = options_list['mapping_rule']
    else:
        mapping_rule = None
    num_of_dates = last_col - start_date_col
    first_label, time_line = date_func(header_row[start_date_col].value,
                                       wb.datemode, num_of_dates)
    IWarehouse.add_time_scale(ssn, series_name, time_line)
    for row_index in range(start_data_row, ws.nrows):
        data_row = ws.row(row_index)
        meta = []
        meta_dict = collections.OrderedDict({})
        for key, val in meta_cols.items():
            meta_dict[val] = data_row[key].value
            meta.append(data_row[key].value)
        if mapping_rule is not None:
            new_meta_dict = mapping(meta_dict, mapping_rule)
            meta = []
            for key, value in new_meta_dict.items():
                meta.append(value)
        # Using db interface
        var_name = data_row[name_col].value
        if var_name in map_names:
            var_name = map_names[var_name]
        entity = IWarehouse.add_entity(ssn, meta)
        variable = entity.force_variable(var_name, 'float')
        time_series = variable.force_time_series(series_name)
        values = []
        for col_index in range(start_date_col, last_col):
            value = data_row[col_index].value
            if value == '':
                value = 0.0
            values.append(value)
        time_series.set_values(first_label, values)
