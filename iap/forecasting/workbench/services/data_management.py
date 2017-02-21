import copy
from ....common.helper import dicts_left_join
from ..helper import VariableType, SlotType, AccessMask
from ..services import help_data_manager as data__service
from ..calculation_kernel import CalculationKernel
from ....common.repository.models_managers import access_manager


def set_entity_values(permission_tree, container, entity_id, values):

    # Get requested entity.
    entity = container.get_entity_by_id(entity_id)
    # Check access.
    for item in values:
        try:

            var = entity.get_variable(item['var_name'])
            if item['slot_type'] & SlotType.time_series:
                ts = var.get_time_series(item['timescale'])

                item_path = ["*-*".join(entity.path), item['var_name'], item['timescale'], item['time_label']]
                mask = access_manager.check_permission(permission_tree, item_path, pointer=0)
                if mask == "Unavailable":
                    continue
                else:
                    time_indexes = access_manager.check_period_perm(mask['tree'], ts_point=item['time_label'])
                    for time_index in time_indexes:
                        ts.set_value_by_index(ts_name=item['timescale'], index=time_index, value = item['value'])
            elif item['slot_type'] & SlotType.scalar:
                scalar = var.get_scalar(item['timescale'])
                scalar.set_value()
            elif item['slot_type'] & SlotType.period_series:

                ps = var.get_periods_series(item['timescale'])
                item_path = ["*-*".join(entity.path), item['var_name'], item['timescale'],
                             item['time_label']]
                mask = access_manager.check_permission(permission_tree, item_path, pointer=0)
                if mask == "Unavailable":
                    continue
                else:
                    time_indexes = access_manager.check_period_perm(mask['tree'], ts_period=item['time_label'])
                    for time_index in time_indexes:
                        ps.set_value(time_index, item['value'])
            else:
                raise Exception
        except KeyError:
            raise Exception
    return


def get_entity_data(permission_tree, container, config, entities_ids, lang):
    # Initialize structure for output.
    entity_data = dict(
        data=dict(
            timescales=None,
            variables=None,
            decomp_types=None,
            timelabels=None,
            variable_values=None,
            change_over_period=None,
            decomp=None,
            factor_drivers=None,
            insights=None,
            decomp_type_factors=None
        ),
        config=None
    )
    # Get requested entities.
    entity_id = entities_ids[0]
    #TODO realise for all entities
    ent = container.get_entity_by_id(entity_id)

    # Define default selector for time periods.
    main_timescales = config.get_property('dash_timescales')
    top_ts_period = config.get_property('dash_top_ts_period')
    dec_timescales = config.get_property('dash_decomposition_timescales')
    top_ts = str(main_timescales[0])
    bottom_ts = str(main_timescales[-1])
    mid = container.timeline.get_period_by_alias(top_ts, 'history')[0][1]
    entity_data['config'] = dict(
        decomp_timescales=[str(x) for x in dec_timescales],
        main_period=dict(timescale=top_ts, start=top_ts_period[0], mid=mid,
                         end=top_ts_period[1]),
        decomp_period=dict(timescale=top_ts, start=mid, end=top_ts_period[1])
    )

    # Get timelabels tree and time borders for every timescale.
    ts_tree, ts_borders = container \
        .timeline.get_timeline_tree(top_ts, bottom_ts, top_ts_period)
    entity_data['data']['timelabels'] = ts_tree

    # Get timescales view settings.
    timescales_info = config.get_objects_properties('timescale', main_timescales, lang)
    timescales_view_info = []


    for ts_info in timescales_info:
        ts_view_props = dict(
            id=None,
            full_name=None,
            short_name=None,
            lag=None
        )
        dicts_left_join(ts_view_props, ts_info)
        ts_view_props['lag'] = \
            container.timeline.get_growth_lag(ts_info[0]['id'])
        timescales_view_info.append(ts_view_props)
    entity_data['data']['timescales'] = timescales_view_info

    # Get time labels for every timescale.
    # Get growth rates periods for every timescale.
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

    # Get variables to view. Values, growth rates, CAGRS.
    vars_view_props = []
    time_series_data = dict([(x, dict()) for x in ts_borders.keys()])
    periods_data = dict([(x, dict()) for x in ts_borders.keys()])

    try:
        items_view_props = config.get_vars_for_view(meta=ent.meta, path=ent.path)
    except Exception:
        raise Exception#TODO change on no var for view


    for item in items_view_props:
        # Get entity to get variables from.
        curr_ent = container.get_entity_by_filter(ent, item['filter'])
        # Collect variables data.
        absent_vars_ids = []
        var_items = item['variables']
        for var_info in var_items:
            var_id = var_info['id']
            var = curr_ent.get_variable(var_id)
            if var is None:
                absent_vars_ids.append(var_info['id'])
                continue


            for ts_name, ts_period in ts_borders.items():


                ts = var.get_time_series(ts_name)

                inner_path = ["*-*".join(ent.path), var_id, ts_name, ts_period]
                mask = access_manager.check_permission(permission_tree, inner_path, pointer=0)
                if mask == "Unavailable":
                    continue
                else:
                    ts_period = access_manager.check_period_perm(mask['tree'], ts_period)
                    for period in ts_period:
                        values = [ts.get_value(time_point)[0] for time_point in period]
                        ps = var.get_periods_series(ts_name)
                        print("Period Series", ps)
                            #check ps
                        time_series_data[ts_name][var_info['id']] = \
                            {time_labels[ts_name][i]: values[i]
                            for i in range(len(values))}
                        periods_data[ts_name][var_info['id']] = \
                            [dict(abs=0, rate=ps.get_value(p), start=p[0], end=p[1]) for p in gr_periods[ts_name]]

        # Get variables properties.
        vars_ids = [var_info['id']
                    for var_info in item['variables']
                    if var_info['id'] not in absent_vars_ids]
        vars_types = [var_info['type']
                      for var_info in item['variables']
                      if var_info['id'] not in absent_vars_ids]

        vars_props = config\
            .get_objects_properties('variable', vars_ids, lang)
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
    entity_data['data']['variable_values'] = time_series_data

    # Get decomposition types properties.
    decs_types_view_props = data__service.get_decs_types_view_props(config, lang)
    entity_data['data']['decomp_types'] = decs_types_view_props

    # Get decomposition.
    dec_periods = {key: value for key, value in gr_periods.items()
                   if key in dec_timescales}

    decomp_data = \
        get_decomposition(container, config, entities_ids, dec_periods)

    decomp_data_for_view = transform_decomp_for_view(decomp_data)


    # Update periods data with decomposition
    for row in decomp_data:
        if row['var_id'] not in periods_data[row['ts_name']]:

            periods_data[row['ts_name']][row['var_id']] = []
        periods_data[row['ts_name']][row['var_id']]\
            .append(dict(abs=row['abs'], rate=row['rate'],
                         start=row['start'], end=row['end']))

    entity_data['data']['decomp'] = decomp_data_for_view
    entity_data['data']['change_over_period'] = periods_data

    # Fill factors for dec type.
    dec_type_factors = data__service.get_factors_for_dec_type(decomp_data_for_view=decomp_data_for_view)
    entity_data['data']['decomp_type_factors'] = dec_type_factors


    # Extend variables properties.
    for item in config.get_decomp_vars_for_view(meta=ent.meta, path=ent.path):
        curr_ent = container.get_entity_by_filter(ent, item['filter'])
        vars_ids = [var_info['id'] for var_info in item['variables']]
        vars_props = \
            config.get_objects_properties('variable', vars_ids, lang)
        for index, v_props in enumerate(vars_props):
            view_props = dict(id=None, full_name=None, short_name=None,
                              type=None, metric=None, format=None, hint='')
            dicts_left_join(view_props, v_props)
            view_props['type'] = 'impact'
            vars_view_props.append(view_props)
    entity_data['data']['variables'] = vars_view_props

    # Relations between factors and drivers
    factor_drivers = config.get_factor_drivers_relations(meta=ent.meta, path=ent.path)
    for factor, fd_rel in factor_drivers.items():
        factor_drivers[factor] = \
            [dict(factor=x[0], driver=x[1]) for x in fd_rel]
    entity_data['data']['factor_drivers'] = factor_drivers

    # Get Insights.
    entity_data['data']['insights'] = [dict(text=x) for x in ent.insights]

    return entity_data


def get_decomposition(container, config, entities_ids, timescales_periods):

    # Get requested entity.
    entity_id = entities_ids[0]
    ent = container.get_entity_by_id(entity_id)

    # Get list of decomposition variables.
    entities_dec_vars = config.get_decomp_vars_for_view(meta=ent.meta, path=ent.path)

    # Collect all decomposition data to the flat list.
    decomp_data = []

    for item in entities_dec_vars:
        # Get entity to get variables from.
        curr_ent = container.get_entity_by_filter(ent, item['filter'])
        for var_info in item['variables']:
            var = curr_ent.get_variable(var_info['id'])
            if var is None:
                continue
            for ts_name, periods in timescales_periods.items():
                ps = var.get_periods_series(ts_name)
                for p in periods:
                    decomp_data.append(
                        dict(ts_name=ts_name, dec_type=var_info['type'],
                             start=p[0], end=p[1], var_id=var_info['id'],
                             abs=0, rate=ps.get_value(p))
                    )
    return decomp_data


def transform_decomp_for_view(decomp_data):
    # Transform flat list to view format.
    decomp_data_for_view = dict()
    for row in decomp_data:
        if row['ts_name'] not in decomp_data_for_view:
            decomp_data_for_view[row['ts_name']] = dict()
        if row['dec_type'] not in decomp_data_for_view[row['ts_name']]:
            decomp_data_for_view[row['ts_name']][row['dec_type']] = []
        decomp_set = decomp_data_for_view[row['ts_name']][row['dec_type']]
        decomp_over_period = None
        for period in decomp_set:
            if period['start'] == row['start'] and period['end'] == row['end']:
                decomp_over_period = period
        if decomp_over_period is None:
            decomp_over_period = dict(
                start=row['start'],
                end=row['end'],
                factors=[]
            )
            decomp_set.append(decomp_over_period)
        decomp_over_period['factors'].append(dict(var_id=row['var_id'],
                                                  abs=0, rate=row['rate']))
    return decomp_data_for_view


def get_cagrs(container, config, entities_ids, timescales_periods):
    # Get requested entity.
    entity_id = entities_ids[0]
    ent = container.get_entity_by_id(entity_id)

    # Get list of variables to calculate cagr.
    items_view_props = config.get_vars_for_view(ent.meta, ent.path)

    # Collect growth.
    growth_over_period = []
    for item in items_view_props:
        # Get entity to get variables from.
        curr_ent = container.get_entity_by_filter(ent, item['filter'])

        # Collect variables data.
        for var_info in item['variables']:
            var = curr_ent.get_variable(var_info['id'])
            if var is None:
                continue
            for ts_name, periods in timescales_periods.items():
                ps = var.get_periods_series(ts_name)
                growth_over_period[ts_name][var_info['id']] = \
                    [dict(abs=0, rate=ps.get_value(p), start=p[0], end=p[1])
                     for p in periods]
    return growth_over_period


def get_simulator_data(permission_tree, container, config, entity_id, lang):
    """
    Get simulator data from workbench

    :param req:
    :type req:
    :param project:
    :type project:
    :param container:
    :type container:
    :param config:
    :type config:
    :param entity_id:
    :type entity_id:
    :param lang:
    :type lang:
    :return:
    :rtype:
    """

    simulator_data = dict(
        properties=dict(
            timeline=None,
            timelable=None,
            variables=None,
            decomposition=None,
        ),
        hierarchy=dict(
            timelable_tree=None,
            drivers_tree=None,
            duetos_tree=None,
            duetos_drivers=None,
            drivers=None
        ),
        data=dict(
            values=dict(
                default="  ",
                custom=None
            ),
        ),
        permissions=dict(
            user_permissions=None,
            data_permissions=None
        )
    )

    #TODO - user_permission
    #TODO - data permission

    #TODO Load Properties
    ent = container.get_entity_by_id(entity_id[0])

    #1.load_properties

    #1.1 Load variable properties

    ##Start of get_var_view_prop
    vars_view_props = data__service._get_var_view_prop(config, ent, lang=lang)
    simulator_data['properties']['variables'] = vars_view_props

    #1.2 Load decomposition properties
    dec_types_props = config.get_objects_properties('decomposition', ['value', 'volume'], lang)
    simulator_data['properties']['decomposition'] = dec_types_props


    #1.3 Load label properties

    ts_tree, ts_borders = data__service.get_ts_tree_and_ts_border(config, container)
    simulator_data['hierarchy']['timelable_tree'] = ts_tree


    time_labels = []
    for ts_name, ts_period in ts_borders.items():
        index = 0
        for point_name in container.timeline.get_names(ts_name, ts_period):
            time_labels.append(dict(name=point_name, timeseries_name=ts_name, id=index))
            index+=1

    simulator_data['properties']['timelable'] = time_labels


    time_labels, gr_periods = data__service.\
        get_growth_period_and_time_label(ts_borders, container)

    # Get growth rates periods for every timescale.

    vars_view_props = []

    time_series_data = dict([(x, dict()) for x in ts_borders.keys()])
    periods_data = dict([(x, dict()) for x in ts_borders.keys()])

    items_view_props = config.get_vars_for_view(meta=ent.meta, path=ent.path)
    for item in items_view_props:
        # Get entity to get variables from.
        curr_ent = container.get_entity_by_filter(ent, item['filter'])

        # Collect variables data.
        absent_vars_ids = []
        for var_info in item['variables']:
            var = curr_ent.get_variable(var_info['id'])
            if var is None:
                absent_vars_ids.append(var_info['id'])
                continue
            data__service.\
                get_time_series_values(ts_borders=ts_borders, var=var, periods_data=periods_data,
                                   time_series_data=time_series_data, var_info=var_info, gr_periods=gr_periods)

        # Get variables properties.
        vars_ids = [var_info['id']
                    for var_info in item['variables']
                    if var_info['id'] not in absent_vars_ids]
        vars_types = [var_info['type']
                      for var_info in item['variables']
                      if var_info['id'] not in absent_vars_ids]

        data__service.\
            get_var_view_prop(config, vars_ids, lang, vars_types, vars_view_props)

    simulator_data['data']['values']['custom'] = time_series_data

    #4.Load user pemission
    #user_permission = security.check_feature_permission(req, project_id="JJOralCare", tool_id="forecast",
                                      #features=["save_scenario", "generate_report"])

    #TODO add for data permission

    #simulator_data['permissions'] = user_permission

    return simulator_data


def get_simulator_value_data(permission_tree, container, config, entity_id, lang):

    ent = container.get_entity_by_id(entity_id[0])

    ts_tree, ts_borders = data__service.get_ts_tree_and_ts_border(config=config, container=container)

    # Get variables to view. Values, growth rates, CAGRS.
    time_series_data = dict([(x, dict()) for x in ts_borders.keys()])
    periods_data = dict([(x, dict()) for x in ts_borders.keys()])

    time_labels, gr_periods = data__service.get_growth_period_and_time_label(ts_borders=ts_borders, container=container)

    try:
        items_view_props = config.get_vars_for_view(meta=ent.meta, path=ent.path)
    except Exception:
        return None
    else:
        for item in items_view_props:
            # Get entity to get variables from.
            curr_ent = container.get_entity_by_filter(ent, item['filter'])

            # Collect variables data.
            absent_vars_ids = []
            for var_info in item['variables']:
                var = curr_ent.get_variable(var_info['id'])
                if var is None:
                    absent_vars_ids.append(var_info['id'])
                    continue

                data__service.get_time_series_values(ts_borders, var, periods_data, time_series_data, var_info, gr_periods)

        custom_data = time_series_data

        return custom_data

