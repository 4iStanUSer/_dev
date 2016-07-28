from iap.repository.warehouse import exceptions as ex
from iap.data_processing.processors.common import date_func, get_last_col, \
    get_cell_range
import collections


def jj_oc_sales(wb, info, meta_cols, name_col_num, dates_info, prop_info):
    ws = wb.sheet_by_index(0)
    output = []
    # Initialize data start
    dates_scale = dates_info['scale']
    header_row_index = info['header_row']
    header_row = ws.row(header_row_index)
    start_data_row = info['data_row']
    start_dates_col = dates_info['start_column']
    end_dates_col = dates_info['end_column']
    if end_dates_col == '':
        end_dates_col = get_last_col(ws, header_row)
    # Rename columns if needed
    for key, val in meta_cols.items():
        if val != '':
            header_row[key].value = val
    header_row = change_dates_names(header_row, start_dates_col,
                                              end_dates_col,
                                              dates_info['date_name_rows'], ws)
    for row_index in range(start_data_row, ws.nrows):
        this_row = ws.row(row_index)
        meta = get_meta(header_row, this_row, meta_cols)
        name = this_row[name_col_num].value
        properties = get_properties(header_row, this_row, prop_info)
        new_row = {'meta': meta, 'name': name, 'properties': properties}
        output.append(new_row)
        # desc_val = str(ws.cell(row_index, 0).value)


def get_values(header_row, row, meta_info):
    meta = collections.OrderedDict()
    for column in meta_info:
        column_name = header_row[column].value
        meta[column_name] = row[column].value
    return meta


def change_dates_names(header_row, start_col, end_col, dates_cols, ws):
    start_row = min(dates_cols)
    end_row = max(dates_cols)
    dates_names_range = get_cell_range(0, start_row, end_col,
                                       end_row + 1, ws)
    for i in range(start_col, end_col):
        new_name = ''
        for idx, val in enumerate(dates_cols):
            if idx == 0:
                new_name = str(dates_names_range[idx][i].value)
            else:
                new_name = new_name + str(' ') + \
                           str(dates_names_range[idx][i].value)
        header_row[i].value = new_name
    return header_row


def get_meta(header_row, row, meta_info):
    meta = collections.OrderedDict()
    for column in meta_info:
        column_name = header_row[column].value
        meta[column_name] = row[column].value
    return meta


def get_properties(header_row, row, prop_info):
    prop = collections.OrderedDict()
    for column in prop_info:
        column_name = header_row[column].value
        prop[column_name] = row[column].value
    return prop
