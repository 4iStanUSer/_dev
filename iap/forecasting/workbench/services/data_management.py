import copy
from ....common import security
from ....common.helper import dicts_left_join
from ..helper import VariableType, SlotType, AccessMask
from ..calculation_kernel import CalculationKernel
from ....common.repository.models_managers import access_manager
PERMISSION_STATUS = False


def set_entity_values(container, entity_id, values):

    # Get requested entity.
    entity = container.get_entity_by_id(entity_id)
    # Check access.
    for item in values:
        try:
            var = entity.get_variable(item['var_name'])
            if item['slot_type'] & SlotType.time_series:
                ts = var.get_time_series(item['timescale'])
                ts.set_value(item['time_label'], item['value'])
            elif item['slot_type'] & SlotType.scalar:
                scalar = var.get_scalar(item['timescale'])
                scalar.set_value()
            elif item['slot_type'] & SlotType.period_series:
                ps = var.get_periods_series(item['timescale'])
                ps.set_value(item['time_label'], item['value'])
            else:
                raise Exception
        except KeyError:
            raise Exception
    return


def get_entity_data(permission_tree, project, container, config, entities_ids, lang):

    #TODO renew permission tree

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


    """
    Check permission vor view ent
    """

    #if '*-*'.join(ent.path) in list(permission_tree.keys()):
    #    pass
    #else:
    #    return "No permission to view ent"

    #Extract variables for view
    try:
        items_view_props = config.get_vars_for_view(meta=ent.meta, path=ent.path)
    except Exception:
        raise Exception#TODO change on no var for view
    for item in iter(items_view_props):
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
                    ts_period = check_period_perm(mask['tree'], ts_period)
                    print(ts_period)
                    for period in ts_period:
                        #ts_period = check_period_perm(_ts_periods, ts_period)
                        values = [ts.get_value(time_point)[0] for time_point in period]
                        #values = ts.get_values_for_period(period)
                        ps = var.get_periods_series(ts_name)

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
    decs_types_view_props = []
    dec_types_props = config.get_objects_properties('decomposition', ['value', 'volume'], lang)
    for dec_type in dec_types_props:
        dec_type_view_props = dict(id=None, full_name=None, short_name=None)
        dicts_left_join(dec_type_view_props, dec_type)
        decs_types_view_props.append(dec_type_view_props)
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
    dec_type_factors = dict()
    if len(decomp_data_for_view) > 0:
        for dec_type, values in next(iter(decomp_data_for_view.values())).items():
            dec_type_factors[dec_type] = [x['var_id'] for x in values[0]['factors']]
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


def get_simulator_data(session, container, config, entity_id, lang):
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

    ent = container.get_entity_by_id(entity_id[0])

    #1.load_properties

    #1.1 Load variable properties
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

    simulator_data['properties']['variables'] = vars_view_props

    #1.2 Load decomposition properties
    dec_types_props = config.get_objects_properties('decomposition', ['value', 'volume'], lang)

    simulator_data['properties']['decomposition'] = dec_types_props

    #1.3 Load label properties
    main_timescales = config.get_property('dash_timescales')
    top_ts_period = config.get_property('dash_top_ts_period')

    top_ts = str(main_timescales[0])
    bottom_ts = str(main_timescales[-1])
    ts_tree, ts_borders = container \
        .timeline.get_timeline_tree(top_ts, bottom_ts, top_ts_period)

    time_labels = []
    for ts_name, ts_period in ts_borders.items():
        index = 0
        for point_name in container.timeline.get_names(ts_name, ts_period):
            time_labels.append(dict(name=point_name, timeseries_name=ts_name, id=index))
            index+=1

    simulator_data['properties']['timelable'] = time_labels

    #1.4 Load timeline properties

    #2.load hierarchy and relationship

    #2.1 Load tree

    top_ts_period = config.get_property('dash_top_ts_period')
    top_ts = str(main_timescales[0])
    bottom_ts = str(main_timescales[-1])
    ts_tree, ts_borders = container \
        .timeline.get_timeline_tree(top_ts, bottom_ts, top_ts_period)

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

    simulator_data['hierarchy']['timelable_tree'] = ts_tree
    #2.2 Load drivers tree

    #3.Load Data

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
            # check accces for variable
            """
            if vars is not None and var_info['id'] in vars.keys():
                if PERMISSION_STATUS==True:
                    _ts = {}
                    PERMISSION_STATUS = True
                elif vars[var_info['id']] == {}:
                    _ts = {}
                    PERMISSION_STATUS = True
                else:
                    _ts = vars[var_info['id']]
                    PERMISSION_STATUS=False
            else:
                _ts = None
                PERMISSION_STATUS=False
                continue
            """

            var = curr_ent.get_variable(var_info['id'])
            if var is None:
                absent_vars_ids.append(var_info['id'])
                continue
            for ts_name, ts_period in ts_borders.items():
                ts = var.get_time_series(ts_name)

                # check timeseries permission
                """
                if ts is not None or PERMISSION_STATUS==True:
                    if PERMISSION_STATUS==True or _ts[ts_name] == {}:
                        _ts_periods = {}
                        PERMISSION_STATUS=True
                    else:
                        PERMISSION_STATUS=False
                        _ts_periods = [timeperiod for timeperiod in list(_ts[ts_name].keys()) if timeperiod!='mask']
                else:
                    PERMISSION_STATUS = False
                    _ts_periods = None
                    continue

                """
                # check timeperiod


                """
                if _ts_periods is not None or PERMISSION_STATUS==True:
                    pass
                elif _ts_period not in _ts_periods:
                    print("No Permission")
                    continue
                """

                values = ts.get_values_for_period(ts_period)
                ps = var.get_periods_series(ts_name)
                # check ps

                time_series_data[ts_name][var_info['id']] = {}
                time_series_data[ts_name][var_info['id']]['values'] = values
                #TODO fill abs_growth, relative growth, cagrs
                time_series_data[ts_name][var_info['id']]['abs_growth'] = [None]
                time_series_data[ts_name][var_info['id']]['relative_growth'] = [None]
                time_series_data[ts_name][var_info['id']]['cagrs'] = [None]

                periods_data[ts_name][var_info['id']] = \
                    [dict(abs=0, rate=ps.get_value(p), start=p[0], end=p[1])
                     for p in gr_periods[ts_name]]

        # Get variables properties.
        vars_ids = [var_info['id']
                    for var_info in item['variables']
                    if var_info['id'] not in absent_vars_ids]
        vars_types = [var_info['type']
                      for var_info in item['variables']
                      if var_info['id'] not in absent_vars_ids]

        vars_props = config \
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
    simulator_data['data']['values']['custom'] = time_series_data

    #4.Load user pemission
    #user_permission = security.check_feature_permission(req, project_id="JJOralCare", tool_id="forecast",
                                      #features=["save_scenario", "generate_report"])

    #TODO add for data permission

    #simulator_data['permissions'] = user_permission

    return simulator_data


def get_simulator_value_data(container, config, entity_id, lang):

    custom_data = dict(
    )

    ent = container.get_entity_by_id(entity_id[0])


    main_timescales = config.get_property('dash_timescales')
    top_ts_period = config.get_property('dash_top_ts_period')

    top_ts = str(main_timescales[0])
    bottom_ts = str(main_timescales[-1])
    ts_tree, ts_borders = container \
        .timeline.get_timeline_tree(top_ts, bottom_ts, top_ts_period)

    # Get variables to view. Values, growth rates, CAGRS.
    vars_view_props = []
    time_series_data = dict([(x, dict()) for x in ts_borders.keys()])
    periods_data = dict([(x, dict()) for x in ts_borders.keys()])

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

    items_view_props = config.get_vars_for_view(meta=ent.meta, path=ent.path)

    for item in items_view_props:
        # Get entity to get variables from.
        curr_ent = container.get_entity_by_filter(ent, item['filter'])

        # Collect variables data.
        absent_vars_ids = []
        for var_info in item['variables']:
            # check accces for variable
            """
            if vars is not None and var_info['id'] in vars.keys():
                if PERMISSION_STATUS==True:
                    _ts = {}
                    PERMISSION_STATUS = True
                elif vars[var_info['id']] == {}:
                    _ts = {}
                    PERMISSION_STATUS = True
                else:
                    _ts = vars[var_info['id']]
                    PERMISSION_STATUS=False
            else:
                _ts = None
                PERMISSION_STATUS=False
                continue
            """

            var = curr_ent.get_variable(var_info['id'])
            if var is None:
                absent_vars_ids.append(var_info['id'])
                continue
            for ts_name, ts_period in ts_borders.items():
                ts = var.get_time_series(ts_name)
                # check timeseries permission
                """
                if ts is not None or PERMISSION_STATUS==True:
                    if PERMISSION_STATUS==True or _ts[ts_name] == {}:
                        _ts_periods = {}
                        PERMISSION_STATUS=True
                    else:
                        PERMISSION_STATUS=False
                        _ts_periods = [timeperiod for timeperiod in list(_ts[ts_name].keys()) if timeperiod!='mask']
                else:
                    PERMISSION_STATUS = False
                    _ts_periods = None
                    continue

                """
                # check timeperiod


                """
                if _ts_periods is not None or PERMISSION_STATUS==True:
                    pass
                elif _ts_period not in _ts_periods:
                    print("No Permission")
                    continue
                """

                values = ts.get_values_for_period(ts_period)
                ps = var.get_periods_series(ts_name)
                # check ps

                time_series_data[ts_name][var_info['id']] = {}
                time_series_data[ts_name][var_info['id']]['values'] = values
                # TODO fill abs_growth, relative growth, cagrs
                time_series_data[ts_name][var_info['id']]['abs_growth'] = None
                time_series_data[ts_name][var_info['id']]['relative_growth'] = None
                time_series_data[ts_name][var_info['id']]['cagrs'] = None
                periods_data[ts_name][var_info['id']] = \
                    [dict(abs=0, rate=ps.get_value(p), start=p[0], end=p[1])
                     for p in gr_periods[ts_name]]

        # Get variables properties.
        vars_ids = [var_info['id']
                    for var_info in item['variables']
                    if var_info['id'] not in absent_vars_ids]
        vars_types = [var_info['type']
                      for var_info in item['variables']
                      if var_info['id'] not in absent_vars_ids]

        vars_props = config \
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
    custom_data = time_series_data

    return custom_data



"""
Support function
"""
def check_period_perm(tree, ts_period):

    correct_ts_period = []
    ts_period = range(int(float(ts_period[0])), int(float(ts_period[1])), 1)
    for _ts_period in [i for i in tree.keys() if i!='mask']:
        _ts_period = _ts_period.split(":")
        _ts = range(int(float(_ts_period[0])), int(float(_ts_period[1])), 1)
        correct_ts_period.append(list(set(ts_period) & set(_ts)))
    print("Correct Period", correct_ts_period)
    return correct_ts_period