from iap.common.repository import exceptions as ex
from iap.data_loading.loading_lib.common import get_last_col
import collections


def jj_oc_data_proc(wb, info, meta_cols, name_col_num, dates_info, prop_info,
                    date_func):
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
    dates_rows = get_dates_rows(dates_info['date_name_rows'], ws)
    for row_index in range(start_data_row, ws.nrows):
        this_row = ws.row(row_index)
        meta = get_meta(header_row, this_row, meta_cols)
        name = this_row[name_col_num].value
        properties = get_properties(header_row, this_row, prop_info)
        values = get_values(dates_rows, date_func, this_row, start_dates_col,
                            end_dates_col)
        new_row = {'meta': meta, 'name': name, 'properties': properties,
                   'values': values}
        output.append(new_row)
        # desc_val = str(ws.cell(row_index, 0).value)
    return output


def get_values(dates_rows_list, dates_func, data_row, start_col, end_col):
    data = []
    for column in range(start_col, end_col):
        date_values = []
        for row in dates_rows_list:
            date_values.append(str(row[column].value).strip())
        this_date = dates_func(date_values)
        data.append((this_date, data_row[column].value))
    return data


def get_dates_rows(dates_rows_list, ws):
    dates_rows = []
    for row_index in dates_rows_list:
        dates_rows.append(ws.row(row_index))
    return dates_rows


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
