import datetime

from .. import timeline_lib as t_lib
from ...common.helper_lib import Meta
from .common import empty_to_zero


def jj_oral_care_init(config, warehouse):
    # Add timescales
    start = datetime.datetime.strptime(config['start_date'],
                                       config['date_format'])
    end = datetime.datetime.strptime(config['end_date'],
                                     config['date_format'])
    timeline = t_lib.generate_timeline('annual', '%Y', start, end)
    warehouse.add_time_scale('annual', timeline)


def jj_oral_care_sales(table, config, warehouse):
    # Read parameters from configuration
    timescale_name = config['timescale']
    row_data_start = config.getint('row_data_start')
    col_data_start = config.getint('col_data_start')
    col_country = config.getint('col_country')
    col_var_name = config.getint('col_var_name')
    col_var_metric = config.getint('col_var_metric')
    # Get first time point
    header = next(table, None)
    text_date = header[col_data_start].strip()
    start_date = datetime.datetime.strptime(text_date, '%Y')
    timescale = warehouse.get_time_scale(timescale_name)
    start_point = timescale.get_label_by_stamp(start_date)
    # Parse file
    for index, row in enumerate(table):
        if index + 1 < row_data_start:
            continue
        # Read data from file
        country = row[col_country].strip()
        var_name = row[col_var_name].strip()
        values = [float(empty_to_zero(row[x].strip()))
                  for x in range(col_data_start, len(row))]
        # Skip empty rows
        if sum(values) == 0:
            continue
        # Add data to DB
        entity = warehouse.get_entity([country, 'JJOralCare', 'Mouthwash'])
        if entity is None:
            entity = warehouse.add_entity([country, 'JJOralCare', 'Mouthwash'],
                                          [Meta('Geography', 'Country'),
                                           Meta('Project', 'Project'),
                                           Meta('Products', 'Category')])
        var = entity.get_variable(var_name)
        if var is None:
            var = entity.force_variable(var_name, 'float')
        time_series = var.get_time_series(timescale_name)
        if time_series is None:
            time_series = var.force_time_series(timescale)
        time_series.set_values(start_point, values)
    return


def jj_oral_care_trends(table, config, warehouse):
    # Read parameters from configuration
    timescale_name = config['timescale']
    row_data_start = config.getint('row_data_start')
    col_data_start = config.getint('col_data_start')
    col_country = config.getint('col_country')
    col_trend_name = config.getint('col_trend_name')
    # Get first time point
    header = next(table, None)
    text_date = header[col_data_start].strip()
    start_date = datetime.datetime.strptime(text_date, '%Y')
    timescale = warehouse.get_time_scale(timescale_name)
    start_point = timescale.get_label_by_stamp(start_date)
    # Parse file
    for index, row in enumerate(table):
        if index + 1 < row_data_start:
            continue
        # Read data from file
        country = row[col_country].strip()
        trend_name = row[col_trend_name].strip()
        values = [float(empty_to_zero(row[x].strip()))
                  for x in range(col_data_start, len(row))]
        # Add data to DB
        entity = warehouse.get_entity([country])
        if entity is None:
            warehouse.add_entity([country], [Meta('Geography', 'Country')])
        var = entity.get_variable(trend_name)
        if var is None:
            var = entity.force_variable(trend_name, 'float')
        time_series = var.get_time_series(timescale_name)
        if time_series is None:
            time_series = var.force_time_series(timescale)
        time_series.set_values(start_point, values)
    return
