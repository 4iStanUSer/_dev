from iap.repository import exceptions as ex
from iap.data_processing.processors.common import date_func, get_cell_range,\
    get_last_col

def jj_extract(wb, meta_cols, data_cols, dates_cols):
    ws = wb.sheet_by_index(0)
    if ws.nrows <=1:
        raise ex.EmptyInputsError('jj_extract')
    header_row = ws.row(0)
    last_col = get_last_col(ws, header_row)
    # Init headers cols: names
    for key, val in meta_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            meta_cols[key] = header_row[key].value 
        new_val =  meta_cols[key]
    for key, val in data_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
        if val == '':
            data_cols[key] = header_row[key].value 
        new_val =  data_cols[key]
    for key, val in dates_cols.items():
        if key >= last_col:
            raise ex.NotExistsError('DataProcessing', 'column', key)
    # Create output: Append data
    output = []
    data = get_cell_range(0, 0, ws.ncols, ws.nrows, ws)
    for row_index in range(1, ws.nrows):
        new_row = {'meta': {}, 'data': {}, 'dates': 0}
        for key, val in meta_cols.items():
            new_row['meta'][val] = data[row_index][key].value
        for key, val in data_cols.items():
            new_row['data'][val] = data[row_index][key].value
        new_row['dates'] = date_func(dates_cols, data[row_index])
        output.append(new_row)
    return output