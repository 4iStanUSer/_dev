from iap.repository.warehouse import exceptions as ex

def date_func(date_cols, data_row, index=-1):
    for key, val in date_cols.items():
        if val == 'campaign':
            return int(data_row[key].value)
        if val == 'N/A':
            if index<0:
                raise ex.WrongArgsError('date_func', 'index')
            return str(data_row[index].value)

def get_cell_range(start_col, start_row, end_col, end_row, ws):
    return [ws.row_slice(row, start_colx=start_col, end_colx=end_col) 
            for row in range(start_row, end_row)]

def get_last_col(ws, header_row):
    last_col = 0
    for col_index in range(len(header_row)):
        if header_row[col_index].ctype == 0:
            last_col = col_index + 1
            break
        if col_index == 0:
            continue
    if last_col == 0:
        last_col = ws.ncols
    return last_col