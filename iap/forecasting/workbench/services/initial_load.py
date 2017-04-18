from ....common.helper import Variable, Meta, is_equal_meta
from ..helper import SlotType

def init_load_container(dev_template, wh, container, config):
    # Initialize time scales.
    timelines_info = dev_template['timelines']
    #1.Get timeseries data
    timelines_properties = dev_template['timelines_properties']
    #2.Get Time Series Properties
    alias = {}
    #3.Form properties
    for i in timelines_properties:
        alias[i["alias"]] = {i['alias name ']:[i['aliase start'], i['aliase end']]}
    properties = [dict(name=i['properties'], growth_lag=i['growth_lag'], id ="0") for i in timelines_info]

    top_ts_points = [dict(name_full=i['name_full'], name_short=i['name_short'], children=[])
                     for i in timelines_info]
    #TODO add children points
    #4.Load Time Line's
    container.timeline.load_timelines(properties,
                                      alias,
                                      top_ts_points)

    gr_periods = []
    #5.Configuration
    #6.Load time series name form configuration
    ts_name = config.get_property('dash_timescales')[0]
    #7.Load period's data from configuration
    cagr_periods = container.timeline\
            .get_carg_periods(ts_name, config.get_property('dash_top_ts_period'))

    gr_periods.extend(cagr_periods)
    gr_periods.extend(container.timeline.get_growth_periods(ts_name))
    # Create container structure
    # Find top entity and run entity init function recursively.
    #top_entity_path = dev_template['top_entity']['path']
    #wh_ent = wh.get_entity(top_entity_path)
    # Get paths of entities to copy
    ent_paths = dev_template['entities']
    for path_info in ent_paths:
        #wh_ent = wh.get_entity(path)
        #if wh_ent is None:
        #    raise Exception

        path = path_info['path']
        metas = [''] * len(path)
        metas[-1] = [path_info['dimension'], path_info['level']]
        container.add_entity(path, metas)

        #_init_entity(dev_template, path, container, gr_periods)

    _add_variables(dev_template['entities_variables'], container, gr_periods)

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


def _add_variables(entities_variables, container, gr_periods):
    for item in entities_variables:
        if 'filter' in item:
            ents = container.get_entities_by_meta(
                Meta(dimension=item['filter'][0], level=item['filter'][1]),
                None)
            for cont_ent in ents:
                var = cont_ent.add_variable(item['id'])
                if int(item['slot']) & SlotType.time_series:
                    var.add_time_series(item['ts'])
                if int(item['slot']) & SlotType.scalar:
                    var.add_scalar(item['ts'])
                if int(item['slot']) & SlotType.period_series:
                    ps = var.add_periods_series(item['ts'])
                    # TODO delete the following row.
                    if item['ts'] == 'annual':
                        [ps.set_value(x, 0) for x in gr_periods]
    return


def _init_entity(dev_template, path_info, container, gr_periods):
    # Clean path

    path = path_info['path']

    metas = ['']* len(path)
    metas[-1] = Meta(dimension=path_info['dimension'], level=path_info['level'])

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
        if cont_ent is None:
            kk = 3

        var = cont_ent.get_variable(item['var_id'])
        if var is None:
            kk = 3
            pass
        elif int(item['slot']) & SlotType.time_series:
            ts = var.get_time_series(item['timescale'])

            ts.set_values_from(item['values'], item['start'])
        elif int(item['slot']) & SlotType.scalar:
            scalar = var.get_scalar(item['timescale'])
            scalar.set_value(item['values'])
    return
