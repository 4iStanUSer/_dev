from ....common.helper import dicts_left_join


def get_var_view_prop(config, ent):
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


def get_factors_for_dec_type(decomp_data_for_view, entity_data):
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