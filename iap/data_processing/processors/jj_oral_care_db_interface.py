from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col, \
    get_cell_range, mapping
from iap.repository.tmp_db_interface import *
import collections


def jj_oral_care_sku(wb, options_list):
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
    this_date = date_func(header_row[start_date_col].value, wb.datemode)
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
        entity = Warehouse.get(meta)
        variable = entity.force_data_by_name(var_name)
        time_series = variable.force_series(series_name)
        values = []
        for col_index in range(start_date_col, last_col):
            values.append(data_row[col_index].value)
        time_series.set_data(this_date, values)
