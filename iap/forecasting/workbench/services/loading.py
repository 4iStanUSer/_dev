from ....common import helper_lib


def init_container(dev_template, wh, container, wh_inputs, wh_outputs):
    # Initialize time scales.
    timelines_info = dev_template['timelines']
    container.load_timelines(timelines_info['names'],
                             timelines_info['alias'],
                             timelines_info['top_ts_points'])
    # Find top entity and run entity init function recursively.
    top_entity_path = dev_template['top_entity']['path']
    wh_ent = wh.get_entity(top_entity_path)
    _init_entity(dev_template, wh_ent, container, wh_inputs, wh_outputs)
    _load_dev_data(dev_template, container)


def _init_entity(dev_template, wh_ent, container, input_rules, output_rules):
    cont_ent = container.add_entity(wh_ent.path, wh_ent.path_meta)
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
    for var_name, timescales in level_params['variables'].items():
        var = cont_ent.force_variable(var_name)
        for ts_name in timescales:
            var.force_time_series(ts_name)
    # Add coefficients.
    for coeff_name, timescales in level_params['coefficients'].items():
        for ts_name in timescales:
            cont_ent.force_coefficient(coeff_name, ts_name)
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
    # Add children
    for child in wh_ent.children:
        _init_entity(dev_template, child, container, input_rules, output_rules)


def _load_dev_data(dev_template, container):
    for item in dev_template['dev_storage']:
        entity = container.get_entity_by_path(item['path'])
        for name, value in item['coefficients'].items():
            # TODO add timescale name (DR)
            entity.set_coeff_value(name, '4-4-5', value)