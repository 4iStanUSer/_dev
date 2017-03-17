import datetime
import pandas as pd
from .. import timeline_lib as t_lib
from ...common.helper import Meta
from .common import empty_to_zero
from .. import data_processing_lib as dp_api


def jj_oral_care_init(config, project):
    """
    Initialisation
    :param config:
    :type config:
    :param project:
    :type project:
    :return:
    :rtype:
    """
    for df in dp_api.collect_data(config['JJOralCare_Sales']):
        project_name = config['JJOralCare_Sales']['project_name']
        df = df[['Market', 'Fact']]
        df.rename(columns={'Market': "Entity", 'Fact': "Variable"},
                       inplace=True)
        df['Project'] = project_name
        project.read(df)


def loader(config, store, project):
    project_name = config['General']['project_name']
    df = pd.concat(store)
    df = df[['Market', 'Fact', 'Value', 'TimePoint']]
    df.rename(columns={'Market': "Entity", 'Fact': "Variable"},
              inplace=True)
    df['Project'] = project_name
    df['TimeSeries'] = 'annual'
    df['TimePoint'] = df['TimePoint']
    df['Value'] = df['Value']
    project.read(df)
    project.save_sql(config)


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
    start_point = warehouse.get_label_by_stamp(timescale, start_date)
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

        var = warehouse.get_ent_variable(entity, var_name)
        if var is None:
            var = warehouse.force_ent_variable(entity, var_name, 'float')
        time_series = warehouse.get_var_time_series(var, timescale_name)
        if time_series is None:
            time_series = warehouse.force_var_time_series(var, timescale)
        warehouse.set_ts_values(time_series, start_point, values)
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
    start_point = warehouse.get_label_by_stamp(timescale, start_date)
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
            entity = warehouse.add_entity([country], [Meta('Geography', 'Country')])

        var = warehouse.get_ent_variable(entity, trend_name)
        #var = entity.get_variable(trend_name)
        if var is None:
            var = warehouse.force_ent_variable(entity, trend_name, 'float')
        time_series = warehouse.get_var_time_series(var, timescale_name)
        if time_series is None:
            time_series = warehouse.force_var_time_series(var, timescale)
        warehouse.set_ts_values(time_series, start_point, values)
    return


