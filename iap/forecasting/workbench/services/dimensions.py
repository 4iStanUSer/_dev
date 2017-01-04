import copy

JOIN_SYMBOL = '|-|-|'


def get_selectors_config(config, lang):

    dimensions = config.get_property('dimensions')
    sel_props = config.get_objects_properties('selector', dimensions, lang)

    selectors_for_view = dict()
    for item in sel_props:

        sel_view_options = dict(
            multiple=item['multiple'],
            type=item['type'],
            icon=item['icon'],
            disabled=False,
            name=item['name'],
            placeholder=item['name']
        )
        selectors_for_view[item['id']] = sel_view_options

    return dict(
        selectors=selectors_for_view,
        order=dimensions)


def get_empty_query(search_index):
    order = search_index['order']
    return {x: [] for x in order}


def build_search_index(container, dim_names):
    direct_index = dict()
    points = []
    for ent in container.top_entities:
        point = dict(node_id=None, coords={x: [] for x in dim_names})
        _add_entity_to_index(ent, point, direct_index, dim_names, points)

    reverse_index = {x['node_id']: x['coords'] for x in points}
    return direct_index, reverse_index


def _add_entity_to_index(entity, curr_point, search_index, dim_names, points):
    curr_point['coords'][entity.meta.dimension].append(entity.name)
    curr_point['node_id'] = entity.id

    points.append(curr_point)

    sub_index = search_index
    for i in range(len(dim_names)):
        dim_path = curr_point['coords'][dim_names[i]]
        if len(dim_path) == 0:
            dim_path = ['total']
            #continue
        key = tuple(dim_path)
        if i < len(dim_names) - 1:
            if key not in sub_index:
                sub_index[key] = dict()
            sub_index = sub_index[key]
        else:
            if key in sub_index:
                raise Exception
            sub_index[key] = curr_point['node_id']
    for child in entity.children:
        new_point = copy.deepcopy(curr_point)
        _add_entity_to_index(child, new_point, search_index, dim_names, points)


def get_options_by_ents(search_index, entities_ids):
    reverse_index = search_index['reverse']
    # Filter entities by list from input.
    ents_coords = [coords for node_id, coords in reverse_index.items()
                   if node_id in entities_ids]
    # Create entity based on coords.
    query = get_empty_query(search_index)
    for ent in ents_coords:
        for dim, coords in ent.items():
            merged_coords = JOIN_SYMBOL.join(coords)
            if merged_coords not in query[dim]:
                query[dim].append(merged_coords)
    opts, ents = search_by_query(search_index, query)
    return opts


def search_by_query(search_index, query):
    order = search_index['order']
    search_indexes = [search_index['direct']]
    options = dict()
    entities_ids = []
    query_internal = _transform(query)
    for i, dim_id in enumerate(order):
        # Collect available options.
        keys = []
        for item in search_indexes:
            keys.extend(item.keys())
        # Get current selection.
        dimension_selection = query_internal.get(dim_id)
        # Verify current selection.
        # If selection is empty or not valid set default selection.
        dimension_selection = [x for x in dimension_selection if x in keys]
        if len(dimension_selection) == 0:
            dimension_selection = [sorted(keys)[0]]
        options[dim_id] = _fill_options(keys, dimension_selection)
        next_iter_indexes = []
        for selected in dimension_selection:
            for curr_search_index in search_indexes:
                search_res = curr_search_index.get(selected)
                if search_res is None:
                    continue
                if i < len(order) - 1:
                    if not isinstance(search_res, dict):
                        raise Exception
                    next_iter_indexes.append(search_res)
                else:
                    if isinstance(search_res, dict):
                        raise Exception
                    entities_ids.append(search_res)
        if len(next_iter_indexes) == 0 and i != len(order) - 1:
            raise Exception
        search_indexes = next_iter_indexes
    return options, entities_ids


def _fill_options(keys_list, selected_items):
    options = dict(
        data=[],
        selected=[JOIN_SYMBOL.join(x) for x in selected_items]
    )
    for item in keys_list:
        if len(item) == 0:
            continue
        elif len(item) == 1:
            item_id = item[-1]
            name = item[-1]
            parent_id = None
        else:
            item_id = JOIN_SYMBOL.join(item)
            name = item[-1]
            parent_id = JOIN_SYMBOL.join(item[:len(item)-1])
        options['data'].append(dict(name=name, id=item_id,
                                    parent_id=parent_id))
    return options


def _transform(query):
    tuppled_query = dict()
    for dim_name, dim_selection in query.items():
        tuppled_query[dim_name] = \
            [tuple(x.split(JOIN_SYMBOL)) for x in dim_selection]
    return tuppled_query
