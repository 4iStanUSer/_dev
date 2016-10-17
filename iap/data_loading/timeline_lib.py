import datetime
from xlrd import xldate_as_tuple
from collections import OrderedDict
from dateutil.relativedelta import relativedelta


def excel_to_date(date_value, date_mode):
    year, month, day, hour, minute, second = xldate_as_tuple(int(date_value),
                                                             date_mode)
    d = datetime.datetime(year=year, month=month, day=day)
    return d


def get_timeline_label(timestamp, timescale):
    pass


def generate_timeline(timescale, date_format, start, end):
    if timescale in ['annual', 'monthly', '4-4-5']:
        # Define time delta
        delta = None
        if timescale == 'annual':
            delta = relativedelta(years=1)
        elif timescale == 'monthly':
            delta = relativedelta(months=1)
        elif timescale == '4-4-5':
            delta = relativedelta(months=1)
        if delta is None:
            raise Exception('Unknown timescale')
        # Generate timeline
        timeline = OrderedDict()
        curr_date = start
        while curr_date <= end:
            label = curr_date.strftime(date_format)
            timeline[label] = curr_date
            curr_date += delta
        return timeline
    elif timescale == 'weekly':
        delta = relativedelta(days=7)
        # Generate timeline
        timeline = OrderedDict()
        curr_date = start
        while curr_date <= end:
            week_number = str(curr_date.date().isocalendar()[1])
            if week_number != 53:
                if len(week_number) == 1:
                    week_number = '0' + week_number
                label = str(curr_date.year) + '_' + week_number
                timeline[label] = curr_date
            curr_date += delta
        return timeline
