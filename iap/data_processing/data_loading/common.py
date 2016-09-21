from iap.repository import exceptions as ex
import datetime
import xlrd
import collections
from iap.repository.db.warehouse import DataType, get_default_value
import math


# TODO delete this old method
def __mapping(in_meta_dict, rules_dict):
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


# time line converter
def tl_weekly_to_month_445(time_stamp, num_of_dates, first_week_num=0):
    first_label = ''
    output = collections.OrderedDict({})
    divider = 4.34
    year = time_stamp.year
    if first_week_num == 0:
        week_num = time_stamp.isocalendar()[1]
    else:
        week_num = first_week_num
    output_months = __get_short_months_with_num_keys()
    for i in range(num_of_dates):
        this_month = week_num/divider
        this_month = math.ceil(this_month)
        # Init vars for month loop
        if this_month > 12:
            year += 1
            this_month -= 12
            week_num = 1
        month_string = output_months[this_month]
        new_key = month_label(month_string, year)
        if new_key not in output:
            output[new_key] = datetime.datetime(year, this_month, 1)
        if i == 0:
            first_label = new_key
        week_num += 1
    return first_label, output


def week_to_month(yyyy, week_num):
    divider = 4.34
    output_months = __get_short_months_with_num_keys()
    this_month = week_num / divider
    this_month = math.ceil(this_month)
    month_string = output_months[this_month]
    date_label = month_label(month_string, yyyy)
    return date_label


def month_label(month_string, yyyy):
    return month_string + ' ' + str(yyyy)


def convert_value(value, data_type):
    if value == '':
        result = get_default_value(DataType[data_type])
        return result
    if data_type == 'float':
        try:
            result = float(value)
        except:
            raise ex.WrongFormatError('float', value, '', 'convert_value')
    elif data_type == 'int':
        try:
            result = int(value)
        except:
            raise ex.WrongFormatError('int', value, '', 'convert_value')
    elif data_type == 'string':
        try:
            result = str(value)
        except:
            raise ex.WrongFormatError('str', value, '', 'convert_value')
    else:
        raise ex.WrongValueError(value, 'DataType', 'Wrong value type',
                                 'convert_value')
    return result


def mapping(in_list_of_dict, rules_dict):
    # Check rules match
    out_meta = []
    for rule in rules_dict:
        input_rule = rule['in']
        is_matched = False
        for dimension_value, name_value in input_rule.items():
            is_matched = False
            for item in in_list_of_dict:
                if item['Dimension_name'] == dimension_value\
                        and item['Name'] == name_value:
                    is_matched = True
                    break
            if not is_matched:
                break
        # generate output meta
        if is_matched:
            # one rule for one row
            out_rule = rule['out']
            change_rule = rule['rule']
            if change_rule == 'rename':
                for item in in_list_of_dict:
                    for dimension_value, name_value in out_rule.items():
                        if item['Dimension_name'] == dimension_value:
                            item['Name'] = name_value
                            break
                return in_list_of_dict, False
            # else we will replace out result using out rule
            for dimension_value, name_value in out_rule.items():
                is_matched = False
                for item in in_list_of_dict:
                    # We will change(map) names if dimension name was matched
                    if item['Dimension_name'] == dimension_value:
                        is_matched = True
                        copy_item = item.copy()
                        break
                if is_matched:
                    copy_item['Name'] = name_value
                    out_meta.append(copy_item)
            return out_meta, True
    return in_list_of_dict, False


def date_monthly_excel_number(date_string, date_mod, num_of_dates):
    output = collections.OrderedDict({})
    first_label = ''
    output_months = __get_short_months_with_num_keys()
    try:
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(
            int(date_string), date_mod)
        for i in range(num_of_dates):
            if month > 12:
                year += 1
                month -= 12
            month_string = output_months[month]
            new_key = month_label(month_string, year)
            output[new_key] = datetime.datetime(year=year, month=month, day=1)
            if i == 0:
                first_label = new_key
            month += 1
        return first_label, output
    except:
        ex.WrongValueError(date_string, 'date as an excel number', '',
                           'date_monthly_excel_number')
        return 0


# TODO delete, not used
def date_func(date_cols, data_row, index=-1):
    for key, val in date_cols.items():
        if val == 'campaign':
            return int(data_row[key].value)
        if val == 'N/A':
            if index < 0:
                raise ex.WrongArgsError('date_func', 'index')
            return str(data_row[index].value)


# TODO update or delete. Not used
def date_yyyyww(date_value, num_of_dates):
    string_date = str(int(date_value))
    time_line = datetime.datetime.strptime(string_date + '-0', "%Y%W-%w")
    year = time_line.year
    week = time_line.isocalendar()[1]
    key = str(year) + ' W' + str(week)
    return key
    # return int(date_value)


def date_year_month(date_values, num_of_dates):
    first_label = ''
    output = collections.OrderedDict({})
    new_year = int(float(date_values[0]))
    month = date_values[1]
    months = __get_months_with_name_keys()
    output_months = __get_short_months_with_num_keys()
    # Init vars for month loop
    new_month_num = months[month.lower()]
    for i in range(num_of_dates):
        if new_month_num > 12:
            new_year += 1
            new_month_num -= 12
        month_string = output_months[new_month_num]
        new_key = month_label(month_string, new_year)
        output[new_key] = datetime.datetime(new_year, new_month_num, 1)
        if i == 0:
            first_label = new_key
        new_month_num += 1
    return first_label, output


def __get_months_with_name_keys():
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
    return months


def __get_short_months_with_num_keys():
    output_months = {1: 'Jan',
                     2: 'Feb',
                     3: 'Mar',
                     4: 'Apr',
                     5: 'May',
                     6: 'Jun',
                     7: 'Jul',
                     8: 'Aug',
                     9: 'Sep',
                     10: 'Oct',
                     11: 'Nov',
                     12: 'Dec'}
    return output_months


def date_yyyymm(date_string):
    year = int(date_string[:3])
    month = int(date_string[4:])
    return datetime.datetime(year=year, month=month, day=1)


def date_mmddyyyy(date_string, num_of_dates):
    date_split = date_string.split('/')
    year = int(date_split[2])
    month_num = int(date_split[1])
    first_label = ''
    output = collections.OrderedDict({})
    output_months = __get_short_months_with_num_keys()
    # Init vars for month loop
    for i in range(num_of_dates):
        if month_num > 12:
            year += 1
            month_num -= 12
        month_string = output_months[month_num]
        new_key = month_label(month_string, year)
        output[new_key] = datetime.datetime(year, month_num, 1)
        if i == 0:
            first_label = new_key
            month_num += 1
    return first_label, output


def date_year(date_values):
    year = int(float(date_values[0]))
    return datetime.datetime(year, 1, 1)


def date_jj_1week(date_string, num_of_dates):
    first_label = ''
    output = collections.OrderedDict({})
    try:
        tmp_split = date_string.split(' ')
        date_split = tmp_split[2].split('/')
        month = int(date_split[0])
        day = int(date_split[1])
        year = int('20' + str(date_split[2]))
        time_stamp = datetime.datetime(year=year, month=month, day=day)
        week = time_stamp.isocalendar()[1]
        for i in range(num_of_dates):
            if week > 52:
                year += 1
                week -= 52
            new_key = str(year) + ' W' + str(week)
            output[new_key] = time_stamp
            if i == 0:
                first_label = new_key
            week += 1
            time_stamp += datetime.timedelta(days=7)
        return first_label, output
    except Exception as err:
        print(err.args)
        return 0


# time line converter
def tl_weekly_to_month_445_str(date_string, num_of_dates, first_week_num=0):
    first_label = ''
    output = collections.OrderedDict({})
    divider = 4.34

    tmp_split = date_string.split(' ')
    date_split = tmp_split[2].split('/')
    month = int(date_split[0])
    day = int(date_split[1])
    year = int('20' + str(date_split[2]))
    time_stamp = datetime.datetime(year=year, month=month, day=day)

    year = time_stamp.year
    if first_week_num == 0:
        week_num = time_stamp.isocalendar()[1]
    else:
        week_num = first_week_num
    output_months = __get_short_months_with_num_keys()
    for i in range(num_of_dates):
        this_month = week_num/divider
        this_month = math.ceil(this_month)
        # Init vars for month loop
        if this_month > 12:
            year += 1
            this_month -= 12
            week_num = 1
        month_string = output_months[this_month]
        new_key = month_label(month_string, year)
        if new_key not in output:
            output[new_key] = datetime.datetime(year, this_month, 1)
        if i == 0:
            first_label = new_key
        week_num += 1
    return first_label, output


def get_cell_range(start_col, start_row, end_col, end_row, ws):
    return [ws.row_slice(row, start_colx=start_col, end_colx=end_col)
            for row in range(start_row, end_row)]
    # return [ws.cell(row, column).value for row in range(start_row, end_row)
    #         for column in range(start_col, end_col)]
    # return [ws.row_values(row, start_colx=start_col, end_colx=end_col)
    #         for row in range(start_row, end_row)]


def get_last_col(data, header_row_index):
    last_col = 0
    for col_index in range(len(data[header_row_index])):
        if data[header_row_index][col_index].ctype == 0:
            last_col = col_index + 1
            break
        if col_index == 0:
            continue
    if last_col == 0:
        last_col = len(data[0])
    return last_col
