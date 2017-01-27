from ....common.helper import is_equal_path


def download_data_from_wh(warehouse, container, mapping):
    # Declare variables.
    wh_entity = None
    cont_entity = None
    prev_wh_entity = None
    prev_cont_entity = None
    for row in mapping:
        # Get warehouse entity if necessary.
        path = []
        warehouse._get_ent_path(prev_wh_entity, path)
        if prev_wh_entity is None or \
                not is_equal_path(path, row['wh_path']):
            wh_entity = warehouse.get_entity(row['wh_path'])
            prev_wh_entity = wh_entity
        # Get container entity if necessary.
        if prev_cont_entity is None or \
                prev_cont_entity.id != row['cont_path']:
            cont_entity = container.get_entity_by_path(row['cont_path'])
            prev_cont_entity = cont_entity

        print(row['cont_ts'], row['time_period'])
        period = container.timeline.get_period_by_alias(row['cont_ts'], row['time_period'])[0]
        # Get data from warehouse.
        try:
            wh_var = wh_entity.get_variable(row['wh_var'])
            if wh_var is None:
                continue
            wh_ts = wh_var.get_time_series(row['wh_ts'])
            if wh_ts is None:
                continue
            values = wh_ts.get_values(period)
            if values is None:
                pass
            # Set data to container.

            var = cont_entity.get_variable(row['cont_var'])
            ts = var.get_time_series(row['cont_ts'])
            ts.set_values_from(values, period[0])
        except AttributeError:
            continue

def upload_data_to_wh(warehouse, container, mapping):
    pass