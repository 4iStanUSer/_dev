from iap.repository import exceptions as ex
from iap.data_processing.processors.common import get_last_col
from iap.repository.tmp_db_interface import *


def jj_brand(wb, info, meta_cols, name_col_num, dates_info, prop_info,
             date_func):
            # wb, meta_cols, data_cols, dates_cols):
    ws = wb.sheet_by_name('Report1')
    output = []
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
    start_date_point = date_func(header_row[start_dates_col].value)
    series_name = dates_info['scale']
    while row_index < ws.nrows:
        desc_val = str(meta_column[row_index].value)
        # Add meta and data to output only if facts exist
        if desc_val.strip().lower() == 'facts':
            last_meta_row = row_index - 1
            last_facts_row = __get_last_facts_row(ws, row_index+1, ws.nrows,
                                                  end_dates_col)
            # Looking for facts by rows and data by columns, add data to db
            # using db interface
            meta = __get_meta(meta_column, start_meta_row, last_meta_row)
            entity = Warehouse.get(meta)
            for row_index in range(row_index+1, last_facts_row + 1):
                data_row = ws.row(row_index)
                fact_name = meta_column[row_index].value
                variable = entity.force_data_by_name(fact_name)
                values = []
                for col_index in range(start_dates_col, end_dates_col):
                    values.append(data_row[col_index].value)
                times_series = variable.force_series(series_name)
                times_series.set_data(start_date_point, values)
            row_index = last_facts_row
            start_meta_row = last_facts_row + 1
        row_index += 1
    return output


def __get_meta(meta_column, start_meta_row, last_meta_row):
    meta = []
    for row_index in range(start_meta_row, last_meta_row + 1):
        desc_val = str(meta_column[row_index].value)
        meta.append(desc_val)
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
