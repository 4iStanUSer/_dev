from ..container.entity_data import VariableType


def get_entity_data(container, config, entity_id):

    def transform_var_type(variable_type):
        if variable_type & VariableType.is_output:
            return 'output'
        if variable_type & VariableType.is_driver:
            return 'driver'
        return None

    # Load configuration parameters.
    try:
        top_ts = config['dashboard_top_ts']
        bottom_ts = config['dashboard_bottom_ts']
        period = config['dashboard_period'][top_ts]
        cagr_periods = config['dashboard_cagr_periods'][top_ts]
    except KeyError:
        raise Exception

    # Define default selection for time periods
    mid = container.timeline.get_period_by_alias(top_ts, 'history')[1]
    main_period = dict(timsecale=top_ts, start=period[0], mid=mid, end=period[1])
    decomp_period = dict(timescale=top_ts, start=mid, end=period[1])
    # Get requested entity.
    #entity_id = entities_ids[0]
    ent = container.get_entity_by_id(entity_id)
    # Get list of timescales.
    ts_tree, ts_borders = container.timeline.get_timeline_tree(top_ts,
                                                               bottom_ts,
                                                               period)
    # Get time labels for every timescale.
    # Get growth rates periods for every timescale.
    time_labels = dict()
    gr_periods = dict()
    for ts_name, ts_period in ts_borders.items():
        time_labels[ts_name] = container.timeline.get_names(ts_name, ts_period)
        gr_periods[ts_name] = \
            container.timeline.get_growth_periods(ts_name, ts_period)
    # Fill output variables properties.
    out_vars_props = dict()
    for var in ent.variables:
        var_type = var.get_property('type')
        if var_type is None:
            continue
        if not (var_type & VariableType.is_output or
                var_type & VariableType.is_driver):
            continue
        out_vars_props[var.name] = \
            dict(name=var.name,
                 metric=var.get_property('metric'),
                 multiplier=var.get_property('mult'),
                 type=transform_var_type(var.get_property('type')))
    # Get CAGRS.
    cagrs = []
    for period in cagr_periods:
        cagrs.extend(_get_entity_cagrs(ent, top_ts, period))
    out_cagrs = dict()
    for item in cagrs:
        if item['var_name'] not in out_cagrs:
            out_cagrs[item['var_name']] = []
        out_cagrs[item['var_name']].append(dict(timescale = top_ts,
                                                start=item['start'],
                                                end=item['end'],
                                                value=item['value']))
    # Get decomposition.
    dec_periods = container.timeline.get_growth_periods(top_ts, ts_borders[top_ts])
    dec_periods.extend(cagr_periods)
    dec_config = config[ent.meta]
    decomposition = [_get_entity_dec(ent, dec_config, top_ts, p)
                     for p in dec_periods]
    # Init structure for output data.
    data = dict([(x, dict()) for x in ts_borders.keys()])
    # Get drivers and outputs from container.
    for var in ent.variables:
        var_type = var.get_property('type')
        if var_type is None:
            continue
        if not (var_type & VariableType.is_output or
                var_type & VariableType.is_driver):
            continue
        for ts_name, ts_period in ts_borders.items():
            ts = var.get_time_series(ts_name)
            ps = var.get_periods_series(ts_name)
            # Fill output data structure.
            values = ts.get_values_for_period(ts_period)
            growth_rates = [ps.get_value(period) for period in gr_periods[ts_name]]
            growth_rates = [0]*(len(values) - len(growth_rates)) + growth_rates
            data[ts_name][var.name] = [
                dict(timestamp=time_labels[ts_name][i], value=values[i],
                     gr=growth_rates[i])
                for i in range(len(values))]

    # Insights.
    insights = [dict(text=x) for x in ent.insights]


    # Return entire entity data.
    result = dict(
        data=dict(timelabels=ts_tree,
                  variables=out_vars_props,
                  data=data,
                  cagrs=out_cagrs,
                  decomposition=decomposition,
                  insights=insights),
        config=dict(main_period=main_period,
                    decomp_period=decomp_period)
    )
    return result


def get_decomposition(container, config, entities_ids, periods):
    # Load configuration parameters.
    try:
        timescale = config['dashboard_top_ts']
    except KeyError:
        raise Exception
    # Get requested entity.
    entity_id = entities_ids[0]
    ent = container.get_entity_by_id(entity_id)
    # Get types of decomposition and list of variables
    dec_config = config[ent.meta]
    # Collect decomposition data.
    all_dec = []
    for p in periods:
        try:
            period_dec = _get_entity_dec(ent, dec_config, timescale, p)
        except Exception:
            period_dec = None
        all_dec.append(period_dec)
    return all_dec


def _get_entity_dec(entity, dec_config, timescale, period):
    decomp_tree = dict(start=period[0], end=period[1])
    for dec_type, dec_vars in dec_config.items():
        decomp_tree[dec_type] = []
        decomp_tree[dec_type].append(dict(name='ini_val', value=1,
                                          growth=0, children=None))
        for var_name in dec_vars:
            var = entity.get_variable(var_name)
            if var is None:
                continue
            ps = var.get_periods_series(timescale)
            value = ps.get_value(period)
            if value is None:
                raise Exception
            decomp_tree[dec_type].append(dict(name=var_name, value=value,
                                              growth=0, children=None))
        decomp_tree[dec_type].append(dict(name='end_val', value=0,
                                          growth=0, children=None))
    return decomp_tree


def get_cagrs(container, config, entities_ids, periods):
    # Load configuration parameters.
    try:
        timescale = config['dashboard_top_ts']
    except KeyError:
        raise Exception
    # Get requested entity.
    entity_id = entities_ids[0]
    ent = container.get_entity_by_id(entity_id)
    all_cagrs = []
    for period in periods:
        try:
            period_cagrs = _get_entity_cagrs(ent, timescale, period)
        except Exception:
            period_cagrs = None
        all_cagrs.extend(period_cagrs)
    out_cagrs = dict()
    for item in all_cagrs:
        if item['var_name'] not in out_cagrs:
            out_cagrs['var_name'] = []
        out_cagrs['var_name'].append(dict(start=item['start'],
                                          end=item['end'],
                                          value=item['value']))
    return out_cagrs


def _get_entity_cagrs(entity, timescale, period):
    cagrs = []
    # Get drivers and outputs from container.
    for var in entity.variables:
        var_type = var.get_property('type')
        if var_type is None:
            continue
        if not (var_type & VariableType.is_output or
                    var_type & VariableType.is_driver):
            continue
        ps = var.get_periods_series(timescale)
        value = ps.get_value(period)
        if value is None:
            raise Exception
        cagrs.append(dict(var_name=var.name,
                          start=period[0],
                          end=period[1],
                          value=value))
    return cagrs
