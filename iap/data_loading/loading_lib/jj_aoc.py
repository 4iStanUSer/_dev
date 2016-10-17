from iap.repository import exceptions as ex
from iap.data_loading.loading_lib.common import date_func, get_last_col


def jj_aoc(wb, meta_cols, data_cols, dates_cols):
    # ws = wb.sheet_by_index(1)
    ws = wb.sheet_by_name('Report1')
    output = []
    # Initialize data start
    data_header_row_index = 0
    start_meta_row = 0
    for row_index in range(ws.nrows):
        desc_val = str(ws.cell(row_index, 0).value)
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
    last_col = get_last_col(ws, header_row)
    # Initialize data: meta table and data table
    row_index = data_header_row_index+1
    meta_column = ws.col(0)
    while row_index < ws.nrows:
        desc_val = str(meta_column[row_index].value)
        # Add meta and data to output only if facts exist
        if desc_val.strip().lower() == 'facts':
            last_meta_row = row_index - 1
            last_facts_row = __get_last_facts_row(ws, row_index+1, ws.nrows, 
                                                  last_col)
            # Looking for rows which go by columns
            for col_index in range(1, last_col):
                new_row = {}
                data_column = ws.col(col_index)
                meta = __get_meta(meta_column, meta_cols, start_meta_row, 
                                  last_meta_row)
                data = __get_data(data_column, meta_column, row_index+1, 
                                  last_facts_row) 
                # Append new_row data
                new_row['meta'] = meta
                new_row['data'] = data
                new_row['dates'] = date_func(dates_cols, header_row, 
                                             index = col_index)
                output.append(new_row)
            row_index = last_facts_row
            start_meta_row = last_facts_row + 1
        row_index = row_index + 1
    return output


def __get_data(data_column, meta_column, start_facts_row, last_facts_row):
    new_data = {}
    for row_index in range(start_facts_row, last_facts_row + 1):
        data_val = data_column[row_index].value
        desc_val = str(meta_column[row_index].value).strip()
        new_data[desc_val] = data_val
    return new_data


def __get_meta(meta_column, meta_cols, start_meta_row, last_meta_row):
    new_meta = {}
    meta_index = 0
    for row_index in range(start_meta_row, last_meta_row + 1):
        desc_val = str(meta_column[row_index].value)
        new_meta[meta_cols[meta_index]] = desc_val
        meta_index = meta_index + 1
    return new_meta


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