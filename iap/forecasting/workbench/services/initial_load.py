from ....common.helper import Variable, Meta, is_equal_meta
from ..helper import SlotType

def init_load_container(dev_template, wh, container, config):
    # Initialize time scales.
    timelines_info = dev_template['timelines']
    container.timeline.load_timelines(timelines_info['properties'],
                             timelines_info['alias'],
                             timelines_info['top_ts_points'])
    gr_periods = []
    for ts_name in dev_template['timelines']['properties'].keys():
        cagr_periods = container.timeline\
            .get_carg_periods(ts_name,
                              config.get_property('dash_top_ts_period'))
        gr_periods.extend(cagr_periods)
        gr_periods.extend(container.timeline.get_growth_periods(ts_name))
    # Create container structure
    # Find top entity and run entity init function recursively.
    #top_entity_path = dev_template['top_entity']['path']
    #wh_ent = wh.get_entity(top_entity_path)
    # Get paths of entities to copy
    ent_paths = dev_template['entities']
    for path in ent_paths:
        wh_ent = wh.get_entity(path)
        if wh_ent is None:
            raise Exception
        _init_entity(dev_template, wh_ent, container, gr_periods)
    # Load developer data
    _load_dev_data(dev_template, container)


def _runner(entity, processor, *args):
    processor(entity, args)
    for child in entity.children:
        _runner(child, args)


def _clean_path(path, metas):
    indexes_to_keep = [i for i in range(len(metas))
                       if metas[i].dimension != 'Project']
    return [x for index, x in enumerate(path) if index in indexes_to_keep],\
           [x for index, x in enumerate(metas) if index in indexes_to_keep]


def _init_entity(dev_template, wh_ent, container, gr_periods):
    # Clean path
    path, metas = _clean_path(wh_ent.path, wh_ent.path_meta)
    cont_ent = container.add_entity(path, metas)
    # Find level parameters in developers template.
    level_params = None
    for item in dev_template['structure']:
        meta = Meta(dimension=item['meta'][0], level=item['meta'][1])
        if is_equal_meta(meta, cont_ent.meta):
            level_params = item
            break
    if level_params is None:
        raise Exception
    # Add variables.
    for var_name, var_info in level_params['variables'].items():
        var = cont_ent.add_variable(var_name)
        if 'props' in var_info:
            for prop_name, prop_val in var_info['props'].items():
                var.set_property(prop_name, prop_val)
        for ts_mode in var_info['timescales']:
            if ts_mode[1] & SlotType.time_series:
                var.add_time_series(ts_mode[0])
            if ts_mode[1] & SlotType.scalar:
                var.add_scalar(ts_mode[0])
            if ts_mode[1] & SlotType.period_series:
                ps = var.add_periods_series(ts_mode[0])
                [ps.set_value(x, 0) for x in gr_periods]
    # Add coefficients.
    for coeff_name, timescales in level_params['coefficients'].items():
        var = cont_ent.add_variable(coeff_name)
        var.add_scalar(timescales[0][0])
    return


def _load_dev_data(dev_template, container):
    for item in dev_template['dev_storage']:
        cont_ent = container.get_entity_by_path(item['path'])
        if 'coefficients' in item:
            for info in item['coefficients']:
                try:
                    var = cont_ent.get_variable(info['name'])
                    scalar = var.get_scalar(info['ts'])
                    scalar.set_value(info['value'])
                except AttributeError:
                    continue
        if 'data' in item:
            for info in item['data']:
                try:
                    var = cont_ent.get_variable(info['name'])
                    ts = var.get_time_series(info['ts'])
                    ts.set_values_from(info['values'], info['start'])
                except AttributeError:
                    continue
        if 'insights' in item:
            for text in item['insights']:
                cont_ent.add_insight(text)

    return
