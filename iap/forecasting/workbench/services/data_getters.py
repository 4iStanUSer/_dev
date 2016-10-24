from ..container.entity_data import VariableType


def get_entity_data(container, config, entity_id):

    def transform_var_type(var_type):
        if var_type & VariableType.is_output:
            return 'output'
        if var_type & VariableType.is_driver:
            return 'driver'
        return None


    # Load configuration parameters.
    try:
        top_ts = config['dashboard_top_ts']
        bottom_ts = config['dashboard_bottom_ts']
        period = config['dashboard_period']
        cagr_periods = config['dashboard_cagr_periods']
    except KeyError:
        raise Exception
    # Declare outputs
    result = dict(timelabels=None,
                  variables=None,
                  data=None,
                  cagrs=None)
    # Get requested entity.
    entity_data = container.get_entity_by_id(entity_id).data
    # Get list of timescales.
    ts_tree, ts_borders = container.timeline.get_timeline_tree(top_ts,
                                                               bottom_ts,
                                                               period)
    # Get time labels for every timescale.
    time_labels = dict()
    for ts_name, ts_period in ts_borders.items():
        time_labels[ts_name] = container.timeline.get_names(ts_name, ts_period)

    # Fill output variables properties.
    var_properties = entity_data.variables_properties
    out_vars_props = {x['name']: dict(name=x['name'],
                                      metric=x['metric'],
                                      multiplier=x['mult'],
                                      type=transform_var_type(x['type']))
                      for x in var_properties}
    # Structure for output data.
    # Structure for cagrs.
    data = dict([(x, dict()) for x in ts_borders.keys()])
    cagrs = dict([(x['name'], None) for x in var_properties])
    # Get data from container.
    for item in var_properties:
        var_name = item['name']
        for ts_name, ts_period in ts_borders.items():
            # p = access.check_permission(entity_id, var.name, ts_name, ts_period)
            # if not p:
            #    continue
            values = entity_data.get_values(var_name, ts_name, ts_period)
            growth_rates = entity_data.get_growth_rates(item['name'], ts_name,
                                                        ts_period)
            # Fill output data structure.
            data[ts_name][var_name] = [dict(timestamp=time_labels[ts_name][i],
                                            value=values[i],
                                            gr=growth_rates[i])
                                       for i in range(len(values))]
            # Fill output cagrs structure
            if ts_name == top_ts:
                cagrs[var_name] = \
                    [dict(start=x[0], end=x[1],
                          value=entity_data.get_growth(var_name, ts_name,
                                                       (x[0], x[1])))
                     for x in cagr_periods]
    # Return entire entity data.
    result['timelabels'] = ts_tree
    result['variables'] = out_vars_props
    result['data'] = data
    result['cagrs'] = cagrs
    return result


def get_decomposition(container, config, entity_id, period):
    # Load configuration parameters.
    try:
        timescale = config['dashboard_top_ts']
    except KeyError:
        raise Exception
    # Get requested entity.
    entity_data = container.get_entity_by_id(entity_id).data
    decomp_tree = entity_data.get_decomposition(timescale, period)
    return decomp_tree


def get_cagrs(container, config, entity_id, period):
    # Load configuration parameters.
    try:
        timescale = config['dashboard_top_ts']
    except KeyError:
        raise Exception
    # Get requested entity.
    entity_data = container.get_entity_by_id(entity_id).data
    cagrs = {x: {'start': period[0],
                 'end': period[1],
                 'value': entity_data.get_growth_over_period(x, timescale,
                                                             period)
                 } for x in entity_data.variables_names}
    return cagrs
