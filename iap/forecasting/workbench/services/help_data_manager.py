from ....common.helper import dicts_left_join
from ....common.repository.models_managers import access_manager

def _get_var_view_prop(config, ent, lang):
    vars_view_props = []
    # Extend variables properties.
    for item in config.get_decomp_vars_for_view(meta=ent.meta, path=ent.path):
        vars_ids = [var_info['id'] for var_info in item['variables']]
        vars_props = \
            config.get_objects_properties('variable', vars_ids, lang)
        for index, v_props in enumerate(vars_props):
            view_props = dict(id=None, full_name=None, short_name=None,
                              type=None, metric=None, format=None, hint='')
            dicts_left_join(view_props, v_props)
            view_props['type'] = 'impact'
            vars_view_props.append(view_props)
    return vars_view_props


def get_factors_for_dec_type(decomp_data_for_view):
    # Fill factors for dec type.
    dec_type_factors = dict()
    if len(decomp_data_for_view) > 0:
        for dec_type, values in next(iter(decomp_data_for_view.values())).items():
            dec_type_factors[dec_type] = [x['var_id'] for x in values[0]['factors']]
    return dec_type_factors


def get_decs_types_view_props(config, lang):
    decs_types_view_props = []
    dec_types_props = config.get_objects_properties('decomposition', ['value', 'volume'], lang)
    for dec_type in dec_types_props:
        dec_type_view_props = dict(id=None, full_name=None, short_name=None)
        dicts_left_join(dec_type_view_props, dec_type)
        decs_types_view_props.append(dec_type_view_props)
    return dec_type_view_props


def get_time_series_values(permission_tree, ent,  ts_borders, var, periods_data, time_series_data, var_info, gr_periods):

    for ts_name, ts_period in ts_borders.items():

        ts = var.get_time_series(ts_name)

        ts_period = [str(i) for i in range(int(float(ts_period[0])), int(float(ts_period[1]))+1,1)]
        index_ts_period = ['0', str(len(ts_period)-1)]

        item_path = ["*-*".join(ent.path), var_info['id'], ts_name, index_ts_period]
        values = []
        stamps = []

        mask = access_manager.check_permission(permission_tree, item_path, pointer=0)
        if mask == "Unavailable":
            continue
        else:
            time_indexes = access_manager.check_period_perm(mask['tree'], ts_period=index_ts_period)
            stamps = [ts_period[i] for i in time_indexes]
            for time_stamp in stamps:
                values.append(ts.get_value(time_stamp)[0])

        ps = var.get_periods_series(ts_name)
        # check ps

        time_series_data[ts_name][var_info['id']] = {}
        time_series_data[ts_name][var_info['id']]['stamps'] = stamps
        time_series_data[ts_name][var_info['id']]['values'] = values
        # TODO fill abs_growth, relative growth, cagrs
        time_series_data[ts_name][var_info['id']]['abs_growth'] = [None]
        time_series_data[ts_name][var_info['id']]['relative_growth'] = [None]
        time_series_data[ts_name][var_info['id']]['cagrs'] = [None]

        periods_data[ts_name][var_info['id']] = \
            [dict(abs=0, rate=ps.get_value(p), start=p[0], end=p[1])
             for p in gr_periods[ts_name]]


def get_var_view_prop(config, vars_ids, lang, vars_types, vars_view_props):

    vars_props = config \
        .get_objects_properties('variable', vars_ids, lang=lang)

    for index, v_props in enumerate(vars_props):
        view_props = dict(
            id=None,
            full_name=None,
            short_name=None,
            type=None,
            metric=None,
            format=None,
            hint=''
        )
        dicts_left_join(view_props, v_props)
        view_props['type'] = vars_types[index]
        vars_view_props.append(view_props)

def get_growth_period_and_time_label(ts_borders, container):

    time_labels = dict()
    gr_periods = dict()
    for ts_name, ts_period in ts_borders.items():
        time_labels[ts_name] = \
            container.timeline.get_names(ts_name, ts_period)
        gr_periods[ts_name] = \
            container.timeline.get_growth_periods(ts_name, ts_period)
        gr_periods[ts_name].extend(
            container.timeline.get_carg_periods(ts_name, ts_period)
        )

    return time_labels, gr_periods

def get_ts_tree_and_ts_border(config, container):

    main_timescales = config.get_property('dash_timescales')
    top_ts_period = config.get_property('dash_top_ts_period')

    top_ts = str(main_timescales[0])
    bottom_ts = str(main_timescales[-1])
    ts_tree, ts_borders = container \
        .timeline.get_timeline_tree(top_ts, bottom_ts, top_ts_period)

    return  ts_tree, ts_borders