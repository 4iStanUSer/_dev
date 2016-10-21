from ....common import helper_lib


def init_configuration(dev_template, config):
    in_config = dev_template.get('configuration', {})
    for key, value in in_config.items():
        config[key] = value


def init_container(dev_template, wh, container, wh_inputs, wh_outputs):
    # Initialize time scales.
    timelines_info = dev_template['timelines']
    container.load_timelines(timelines_info['names'],
                             timelines_info['alias'],
                             timelines_info['top_ts_points'])
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
        _init_entity(dev_template, wh_ent, container, wh_inputs, wh_outputs)
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


def _init_entity(dev_template, wh_ent, container, input_rules, output_rules):
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
    entity_data = cont_ent.data
    # Add variables.
    for var_name, timescales in level_params['variables'].items():
        entity_data.add_variable(var_name, None)
        for ts_name in timescales:
            entity_data.add_time_series(var_name, ts_name)
    # Add coefficients.
    for coeff_name, timescales in level_params['coefficients'].items():
        entity_data.add_coefficient(coeff_name)
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
    #for child in wh_ent.children:
    #   _init_entity(dev_template, child, container, input_rules, output_rules)


def _load_dev_data(dev_template, container):
    for item in dev_template['dev_storage']:
        entity_data = container.get_entity_by_path(item['path']).data
        for info in item['coefficients']:
            # TODO add timescale name (DR)
            entity_data.set_coeff_value(info['name'], info['ts'], info['value'])