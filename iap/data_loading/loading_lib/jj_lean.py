import datetime
import json
from operator import add
from numpy import mean

from .. import timeline_lib as t_lib
from .. import data_processing_lib as dp_lib
from ...common.helper_lib import Meta
from .common import empty_to_zero

def jj_lean_init(config, warehouse):
    # Add root entity
    warehouse.add_entity(['US', 'JJLean'], [Meta('Geography', 'Country'),
                                            Meta('Project', 'Project')])
    # Add timescales
    start = datetime.datetime.strptime(config['start_date'],
                                       config['date_format'])
    end = datetime.datetime.strptime(config['end_date'],
                                     config['date_format'])
    timescales = [
        ('annual', '%Y'),
        ('monthly', '%b-%y'),
        ('4-4-5', '%b-%y'),
        ('weekly', '%y-%W')
    ]
    for t in timescales:
        timeline = t_lib.generate_timeline(t[0], t[1], start, end)
        warehouse.add_time_scale(t[0], timeline)
    return


def jj_lean_media_spend(book, config, warehouse):
    # Read parameters from configuration
    timescale_name = config['timescale']
    col_brand = config.getint('col_brand')
    col_var_name = config.getint('col_var_name')
    col_data_start = config.getint('col_data_start')
    row_data_start = config.getint('row_data_start')
    row_date = config.getint('row_date')
    sheet_index = config.getint('sheet_index')
    # Get ini entity
    parent_entity = warehouse.get_entity(['US', 'JJLean'])
    # Get worksheet
    sheet = book.sheet_by_index(sheet_index)
    # Get first time point
    excel_date = sheet.cell_value(rowx=row_date, colx=col_data_start)
    start_date = t_lib.excel_to_date(excel_date, book.datemode)
    timescale = warehouse.get_time_scale(timescale_name)
    start_point = timescale.get_label_by_stamp(start_date)
    # Parse file
    for row_index in range(row_data_start, sheet.nrows):
        # Read data from file
        row = sheet.row_slice(row_index, start_colx=0, end_colx=sheet.ncols)
        brand_name = row[col_brand].value
        var_name = row[col_var_name].value
        values = [float(empty_to_zero(row[x].value))
                  for x in range(col_data_start, len(row))]
        # Add data to DB
        brand_entity = parent_entity.get_child(brand_name)
        if brand_entity is None:
            brand_entity = parent_entity.add_child(brand_name,
                                                   Meta('Products', 'Brand'))
        var = brand_entity.get_variable(var_name)
        if var is None:
            var = brand_entity.force_variable(var_name, 'float')
        time_series = var.get_time_series(timescale_name)
        if time_series is None:
            time_series = var.force_time_series(timescale)
        time_series.set_values(start_point, values)
    return


def jj_lean_nielsen(book, config, warehouse):
    # Read parameters from configuration
    timescale_name = config['timescale']
    col_data_start = config.getint('col_data_start')
    row_data_start = config.getint('row_data_start')
    row_date = config.getint('row_date')
    sheet_name = config['sheet_name']
    meta_mapping = json.loads(config['meta_mapping'])
    var_mapping = json.loads(config['var_mapping'])
    # Define meta for warehouse tree
    metas = [
        Meta('Geography', 'Country'),
        Meta('Project', 'Project'),
        Meta('Products', 'Brand'),
        Meta('Products', 'Segment'),
        Meta('Chanel Distribution', 'Chanel')
    ]
    # Get worksheet
    sheet = book.sheet_by_name(sheet_name)
    # Get first time point
    full_text_data = str(sheet.cell_value(rowx=row_date, colx=col_data_start))
    text_date = full_text_data[len(full_text_data) - 8:]
    start_date = datetime.datetime.strptime(text_date, '%m/%d/%y')
    timescale = warehouse.get_time_scale(timescale_name)
    start_point = timescale.get_label_by_stamp(start_date)
    # Parse file
    prev_meta = []
    curr_meta = []
    entity = None
    for row_index in range(row_data_start, sheet.nrows):
        # Read data from file
        row = sheet.row_slice(row_index, start_colx=0, end_colx=sheet.ncols)
        first_col_value = row[0].value.strip().lower()
        is_meta_row = row[col_data_start].value == ''
        if is_meta_row:
            # Collect meta
            if first_col_value != 'facts':
                curr_meta.append(first_col_value)
            else:
                # Value 'facts' means that meta is ended and data rows will
                # start from the next line
                # If meta is shorter than previous one, that means
                # meta changed partially and previous meta should be updated
                #  with current.
                if len(curr_meta) < len(prev_meta):
                    curr_meta = \
                        prev_meta[:len(prev_meta) - len(curr_meta)] + curr_meta
                prev_meta = curr_meta
                # Meta mapping
                final_meta = [curr_meta[2], curr_meta[3], curr_meta[0]]
                if len(final_meta) == len(meta_mapping):
                    for i in range(len(final_meta)):
                        final_meta[i] = meta_mapping[i].get(final_meta[i],
                                                            final_meta[i])
                # Get/create entity
                entity = warehouse.get_entity(['US', 'JJLean'] + final_meta)
                if entity is None:
                    is_new = True
                    entity = warehouse.add_entity(['US', 'JJLean'] + final_meta, metas)
                # Clear meta variable
                curr_meta = []
        else:
            # Read data from file
            new_values = [float(empty_to_zero(row[x].value))
                          for x in range(col_data_start, len(row))]
            # Map variable name
            var_name = var_mapping.get(first_col_value, None)
            if var_name is None:
                continue
            # Add data to DB. Set new values or update previous if
            # this is not first occurrence of variable for current entity.
            var = entity.get_variable(var_name)
            if var is None:
                var = entity.force_variable(var_name, 'float')
            time_series = var.get_time_series(timescale_name)
            if time_series is None:
                time_series = var.force_time_series(timescale)
                time_series.set_values(start_point, new_values)
            else:
                old_values = time_series.get_values(start_point)
                upd_values = list(map(add, old_values, new_values))
                time_series.set_values(start_point, upd_values)
    return


def jj_lean_aggr_weeks(config, warehouse):
    def _runner(node, func, timescale, start_point):
        func(node, timescale, start_point)
        for child in node.children:
            _runner(child, func, timescale, start_point)

    def _worker(entity, timescale, start_point):
        for var in entity.variables:
            if var.name in ['% ACV', 'TDP']:
                aggregator = sum
            else:
                aggregator = mean
            time_series_weekly = var.get_time_series('weekly')
            time_series_445 = var.get_time_series('4-4-5')
            if time_series_445 is None and time_series_weekly is not None:
                values_weekly = time_series_weekly.get_values()
                values_445 = dp_lib.weeks_to_445(values_weekly, aggregator)

                time_series_445 = var.get_time_series('4-4-5')
                if time_series_445 is None:
                    time_series_445 = var.force_time_series(timescale)
                time_series_445.set_values(start_point, values_445)

    timescale = warehouse.get_time_scale('4-4-5')
    start_point = timescale.timeline[0].name
    parent_entity = warehouse.get_entity(['US'])
    _runner(parent_entity, _worker, timescale, start_point)










