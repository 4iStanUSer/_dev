from ....common import helper_lib


def download_data_from_wh(warehouse, container, mapping):
    # Declare variables.
    wh_entity = None
    cont_entity = None
    prev_wh_entity = None
    prev_cont_entity = None
    for row in mapping:
        # Get warehouse entity if necessary.
        if prev_wh_entity is None or \
                not helper_lib.is_equal_path(prev_wh_entity.path, row['wh_path']):
            wh_entity = warehouse.get_entity(row['wh_path'])
            prev_wh_entity = wh_entity
        # Get container entity if necessary.
        if prev_cont_entity is None or \
                prev_cont_entity.id != row['cont_entity_id']:
            cont_entity = container.get_entity_by_id(row['cont_entity_id'])
            prev_cont_entity = cont_entity

        period = container.timeline.get_period_by_alias(row['cont_var'].timescale, row['time_period'])[0]
        # Get data from warehouse.
        try:
            wh_var = wh_entity.get_variable(row['wh_var'].variable)
            if wh_var is None:
                continue
            wh_ts = wh_var.get_time_series(row['wh_var'].timescale)
            if wh_ts is None:
                continue
            values = wh_ts.get_values(period)
            # Set data to container.

            var = cont_entity.get_variable(row['cont_var'].variable)
            ts = var.get_time_series(row['cont_var'].timescale)
            ts.set_values_from(values, period[0])
        except AttributeError:
            continue

def upload_data_to_wh(warehouse, container, mapping):
    pass