from iap.repository import exceptions as ex
import datetime
import xlrd


def mapping(in_meta_dict, rules_dict):
    # Check rules match
    for rule in rules_dict:
        is_matched = True
        input_rule = rule['in']
        for meta_name, value in input_rule.items():
            if meta_name not in in_meta_dict:
                is_matched = False
                break
            elif value != in_meta_dict[meta_name]:
                is_matched = False
                break
        # generate output meta dict
        if is_matched:
            out_meta = rule['out']
            return out_meta
    return in_meta_dict


def date_excel_number(date_string, date_mod):
    try:
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(
            int(date_string), date_mod)
        return datetime.datetime(year=year, month=month, day=day)
    except Exception as err:
        print(err.args)
        return 0


def date_func(date_cols, data_row, index=-1):
    for key, val in date_cols.items():
        if val == 'campaign':
            return int(data_row[key].value)
        if val == 'N/A':
            if index < 0:
                raise ex.WrongArgsError('date_func', 'index')
            return str(data_row[index].value)


def date_yyyyww(date_value):
    return int(date_value)


def date_year_month(date_values):
    year = int(float(date_values[0]))
    month = date_values[1]
    months = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'july': 7,
              'august': 8,
              'september': 9,
              'october': 10,
              'november': 11,
              'december': 12}
    month_num = months[month.lower()]
    return datetime.datetime(year, month_num, 1)


def date_yyyymm(date_string):
    year = int(date_string[:3])
    month = int(date_string[4:])
    return datetime.datetime(year=year, month=month, day=1)


def date_year(date_values):
    year = int(float(date_values[0]))
    return datetime.datetime(year, 1, 1)


def date_jj_1week(date_string):
    try:
        tmp_split = date_string.split(' ')
        date_split = tmp_split[2].split('/')
        month = int(date_split[0])
        day = int(date_split[1])
        year = int('20' + str(date_split[2]))
        return datetime.datetime(year=year, month=month, day=day)
    except Exception as err:
        print(err.args)
        return 0


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
