from ....common import helper_lib


def init_calc_engine(calc_engine, instructions):
    calc_engine.load_instructions(instructions, None)


def init_configuration(dev_template, config):
    in_config = dev_template.get('configuration', {})
    for key, value in in_config.items():
        config[key] = value
    for item in dev_template['structure']:
        if 'decomposition' in item:
            meta = helper_lib.Meta(item['meta'][0], item['meta'][1])
            config[meta] = item['decomposition']


def init_container(dev_template, wh, container, config, wh_inputs, wh_outputs):
    # Initialize time scales.
    timelines_info = dev_template['timelines']
    container.timeline.load_timelines(timelines_info['names'],
                             timelines_info['alias'],
                             timelines_info['top_ts_points'])
    gr_periods = []
    for ts_name in dev_template['timelines']['names']:
        gr_periods.extend(config['dashboard_cagr_periods'][ts_name])
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
        _init_entity(dev_template, wh_ent, container, gr_periods, wh_inputs, wh_outputs)
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


def _init_entity(dev_template, wh_ent, container, gr_periods, input_rules, output_rules):
    # Clean path
    path, metas = _clean_path(wh_ent.path, wh_ent.path_meta)
    cont_ent = container.add_entity(path, metas)
    # Find level parameters in developers template.
    level_params = None
    for item in dev_template['structure']:
        meta = helper_lib.Meta(item['meta'][0], item['meta'][1])
        if helper_lib.is_equal_meta(meta, cont_ent.meta):
            level_params = item
            break
    if level_params is None:
        raise Exception
    # Add variables.
    for var_name, var_info in level_params['variables'].items():
        var = cont_ent.add_variable(var_name)
        for prop_name, prop_val in var_info['props'].items():
            var.set_property(prop_name, prop_val)
        for ts_mode in var_info['timescales']:
            if ts_mode[1] & 1:
                var.add_time_series(ts_mode[0])
            if ts_mode[1] & 2:
                var.add_scalar(ts_mode[0])
            if ts_mode[1] & 4:
                ps = var.add_periods_series(ts_mode[0])
                [ps.set_value(x, 0) for x in gr_periods]
    # Add coefficients.
    for coeff_name, timescales in level_params['coefficients'].items():
        var = cont_ent.add_variable(coeff_name)
        var.add_scalar(timescales[0][0])
    # Find exchange mapping rules in developer template.
    exchange_params = None
    for item in dev_template['exchange_rules']:
        meta = helper_lib.Meta(item['meta'][0], item['meta'][1])
        if helper_lib.is_equal_meta(meta, cont_ent.meta):
            exchange_params = item
            break
    if exchange_params is not None:
        inputs_len = len(exchange_params['input_variables'])
        rules = exchange_params['input_variables'] + \
                exchange_params['output_variables']
        for counter, rule in enumerate(rules):
            row = dict(wh_path=wh_ent.path,
                       wh_var=helper_lib.Variable(rule['wh_var'], rule['wh_ts']),
                       cont_entity_id=cont_ent.id,
                       cont_var=helper_lib.Variable(rule['cont_var'],
                                                 rule['cont_ts']),
                       time_period=rule['time_period'])
            if counter < inputs_len:
                input_rules.append(row)
            else:
                output_rules.append(row)
    return


def _load_dev_data(dev_template, container):
    for item in dev_template['dev_storage']:
        cont_ent = container.get_entity_by_path(item['path'])
        if 'coefficients' in item:
            for info in item['coefficients']:
                var = cont_ent.get_variable(info['name'])
                scalar = var.get_scalar(info['ts'])
                scalar.set_value(info['value'])
        if 'data' in item:
            for info in item['data']:
                var = cont_ent.get_variable(info['name'])
                ts = var.get_time_series(info['ts'])
                ts.set_values_from(info['values'], info['start'])
        if 'insights' in item:
            for text in item['insights']:
                cont_ent.add_insight(text)
