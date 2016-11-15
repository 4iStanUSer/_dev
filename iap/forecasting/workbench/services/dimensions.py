import copy

JOIN_SYMBOL = '|-|-|'

def build_search_index(container, dim_names):
    search_index = dict()
    for ent in container.top_entities:
        point = dict(node_id=None, coords={x: [] for x in dim_names})
        _add_entity_to_index(ent, point, search_index, dim_names)
    return search_index


def _add_entity_to_index(entity, curr_point, search_index, dim_names):
    curr_point['coords'][entity.meta.dimension].append(entity.name)
    curr_point['node_id'] = entity.id
    sub_index = search_index
    for i in range(len(dim_names)):
        dim_path = curr_point['coords'][dim_names[i]]
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
        new_point = copy.copy(curr_point)
        _add_entity_to_index(child, new_point, search_index, dim_names)


def search_by_query(search_index, query):
    query = _transform_query(query)
    options = []
    entities_ids = []
    search_indexes = [search_index]
    for i in range(len(query)):
        dimension_selection = query[i]
        if len(dimension_selection) == 0:
                keys = []
                for item in search_indexes:
                    keys.extend(item.keys())
                dimension_selection = [keys[0]]
                options.append(_fill_options(keys, keys[0]))
        next_iter_indexes = []
        for selected in dimension_selection:
            for curr_search_index in search_indexes:
                search_res = curr_search_index.get(selected)
                if search_res is None:
                    continue
                if i < len(query) - 1:
                    if not isinstance(search_res, dict):
                        raise Exception
                    next_iter_indexes.append(search_res)
                else:
                    if isinstance(search_res, dict):
                        raise Exception
                    entities_ids.append(search_res)
        if len(next_iter_indexes) == 0 and i != len(query) - 1:
            raise Exception
        search_indexes = next_iter_indexes
    return options, entities_ids


def _fill_options(keys_list, selected):
    options = dict(data=[], selected=[JOIN_SYMBOL.join(selected)])
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


def _transform_query(query):
    for i in range(len(query)):
        for j in range(len(query[i])):
            if query[i][j] is not None:
                query[i][j] = tuple(query[i][j].split(JOIN_SYMBOL))
    return query
