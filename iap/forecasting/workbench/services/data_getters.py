def get_entity_data(container, entity_id):

    # TODO Load from configuration (DR).
    top_ts = 'Annual'
    bottom_ts = '4-4-5'
    period = (2013, 2020)
    cagr_periods = [(2013, 2015), (2015, 2020)]
    # Declare outputs
    result = dict(timelabels=None,
                  variables=None,
                  data=None,
                  cagrs=None)
    # Get requested entity.
    entity = container.get_entity_by_id(entity_id)
    # Get list of timescales.
    ts_tree, ts_borders = container.timeline.get_timeline_tree(top_ts,
                                                               bottom_ts,
                                                               period)
    # Get time labels for every timescale.
    time_labels = dict()
    for ts_name, ts_period in ts_borders.items():
        time_labels [ts_name] = container.timeline.get_names(ts_name, ts_period)

    # Fill output variables properties.
    var_properties = entity.get_vars_properties()
    out_vars_props = []
    for var_info in var_properties:
        out_vars_props.append(dict(name=var_info['name'],
                                   metric=var_info['metric'],
                                   multiplier=var_info['mult'],
                                   type=var_info['type']))
    # Structure for output data.
    # Structure for cagrs.
    data = dict([(x, dict()) for x in ts_borders.keys()])
    cagrs = dict([(x['name'], None) for x in var_properties])
    # Get data from container.
    for var_info in var_properties:
        var = entity.get_variable(var_info['name'])
        for ts_name, ts_period in ts_borders.items():
            #p = access.check_permission(entity_id, var.name, ts_name, ts_period)
            #if not p:
            #    continue
            ts = var.get_time_scale(ts_name)
            values = ts.get_values(ts_period)
            growth_rates = ts.get_growth_rates(ts_period)

            # Fill output data structure.
            var_points = data[ts_name].get(var.name)
            if var_points is None:
                var_points = []
                data[ts_name][var.name] = var_points
            labels = time_labels[ts_name]
            gr_delay = len(values) - len(growth_rates)
            for i in range(labels):
                if i >= gr_delay:
                    curr_gr = growth_rates[i - gr_delay]
                else:
                    curr_gr = 0
                var_points.append(dict(timestamp=labels[i], value=values[i],
                                       gr=curr_gr))
            # Fill output cagrs structure
            var_cagrs_list = cagrs[var.name]
            if ts_name == top_ts:
                for c_per in cagr_periods:
                    cagr_val = ts.get_cagr(c_per)
                    var_cagrs_list.append(dict(start=c_per[0],
                                               end=c_per[1],
                                               value=cagr_val))
    # Return entire entity data.
    result['timelabels'] = ts_tree
    result['variables'] = out_vars_props
    result['data'] = data
    result['cagrs'] = cagrs
    return result


def get_decomposition(container, entity_id, period):
    # TODO Load from configuration (DR).
    top_ts = 'Annual'
    timescale = top_ts
    # Get requested entity.
    entity = container.get_entity_by_id(entity_id)
    decomp_tree = entity.get_decomposition(timescale, period)
    return decomp_tree


def get_cagrs(container, entity_id, period):
    # TODO Load from configuration (DR).
    top_ts = 'Annual'
    timescale = top_ts
    # Get requested entity.
    entity = container.get_entity_by_id(entity_id)

    cagrs = dict()
    var_properties = entity.get_vars_properties()
    for var_info in var_properties:
        var = entity.get_variable(var_info['name'])
        cagrs[var.name] = []
        ts = var.get_time_scale(timescale)
        cagr_val = ts.get_cagr(period)
        cagrs[var.name].append(dict(start=period[0], end=period[1],
                                    value=cagr_val))
    return cagrs