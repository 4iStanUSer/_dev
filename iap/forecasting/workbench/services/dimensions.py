import copy
from collections import OrderedDict
JOIN_SYMBOL = '|-|-|'


def get_selectors_config(config, lang):
    """
    GET SELECTORS CONFIGURATION

    :param config:
    :type config:
    :param lang:
    :type lang:
    :return:
    :rtype:
    """

    dimensions = config.get_property('dimensions')
    sel_props = config.get_objects_properties('selector', dimensions, lang)
    selectors_for_view = dict()
    for i in sel_props:
        item = i[0]
        sel_view_options = dict(
            multiple=item['multiple'],
            type=item['type'],
            icon=item['icon'],
            disabled=False,
            name=item['id'],#item['name']
            placeholder=item['id']#item['name']
        )
        selectors_for_view[item['id']] = sel_view_options

    return dict(selectors=selectors_for_view, order=dimensions)


def get_empty_query(search_index):
    """
    GET EMPTY QUERY

    :param search_index:
    :type search_index:
    :return:
    :rtype:
    """
    order = search_index['order']
    return {x: [] for x in order}


def build_search_index(container, dim_names):
    """
    BUILD SEARCH INDEX

    Get list of all pathes from container by dimension names


    Dim Name's  - ['geography', 'products']

    :param container:
    :type container:
    :param dim_names:
    :type dim_names:
    :return:
    :rtype:

    Iterate through the top entities
    on every step call _add_entity_to_index()
    """
    direct_index = dict()
    points = []
    for ent in container.top_entities:
        #if ent.variable is not None:
        #    informative = True
        #else:
        #    informative = False
        point = dict(node_id=None, coords={x: [] for x in dim_names})
        _add_entity_to_index(ent, point, direct_index, dim_names, points)

    reverse_index = {x['node_id']: x['coords'] for x in points}
    return direct_index, reverse_index



def _add_entity_to_index(entity, curr_point, search_index, dim_names, points):
    """
    ADD ENTITY BY INDEX

    Recursivelly call

    fill curr_point information - dict(node_id: entity.id, coords={x: [entity.name] for x in dim_names})
    append points list


    :param entity:
    :type entity:
    :param curr_point:
    point = dict(node_id=None, coords={x: [] for x in dim_names})
    :type curr_point:
    :param search_index:
    :type search_index:
    :param dim_names:
    :type dim_names:
    :param points:
    :type points:
    :return:
    :rtype:
    """
    if entity.meta.dimension in dim_names:
        curr_point['coords'][entity.meta.dimension].append(entity.name)

        #curr_point['coords'][entity.meta.dimension] = []
        #curr_point['coords'][entity.meta.dimension].append(entity.name)
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
    else:
        pass


def ents_by_options(options, container):
    """
    {'geography': {'selected': ['australia'],
                    'data': [
                            {'parent_id': None, 'name': 'mexico', 'id': 'mexico'},
                            {'parent_id': None, 'name': 'brazil', 'id': 'brazil'},
                            {'parent_id': None, 'name': 'italy', 'id': 'italy'},
                            {'parent_id': None, 'name': 'australia', 'id': 'australia'},
                            {'parent_id': None, 'name': 'uk', 'id': 'uk'},
                            {'parent_id': None, 'name': 'japan', 'id': 'japan'},
                            {'parent_id': None, 'name': 'spain', 'id': 'spain'},
                            {'parent_id': None, 'name': 'germany', 'id': 'germany'},
                            {'parent_id': None, 'name': 'us', 'id': 'us'},
                            {'parent_id': None, 'name': 'canada', 'id': 'canada'}]},
    'market': {'selected': ['total'],
                'data': [
                        {'parent_id': None, 'name': 'total', 'id': 'total'}]},
    'products': {'selected': ['mouthwash'],
                'data': [{'parent_id': None, 'name': 'mouthwash', 'id': 'mouthwash'},
                         {'parent_id': None, 'name': 'total', 'id': 'total'}]},

    'products2': {'selected': ['total'], 'data': [{'parent_id': None, 'name': 'total', 'id': 'total'}]}}
    :param opts:
    :type opts:
    :return:
    :rtype:
    """
    path = {}
    dimensions = list(options.keys())
    for i in dimensions:
        path[i] = options[i]['selected']


def get_options_by_ents(search_index, entities_ids, lang):
    """
    Return Options by input entities id's

    Attr:

    SEARCH INDEX
    ENTITIES IDS

    :param search_index:
    :type search_index:
    :param entities_ids:
    :type entities_ids:
    :return:
    :rtype:

    """

    reverse_index = search_index['reverse']

    # Get entities coordinates
    #Entities coordinates


    ents_coords = [coords for node_id, coords in reverse_index.items()
                   if node_id in entities_ids]

    # Create entity based on coords.
    query = get_empty_query(search_index)
    #for entities in ents-coords
    for ent in ents_coords:
        #for dim, coords om ent.items
        for dim, coords in ent.items():
            merged_coords = JOIN_SYMBOL.join(coords)
            #if merged selected dimension == []
            if merged_coords not in query[dim]:
                if query[dim]==[]:
                    query[dim].append(merged_coords)
                else:
                    query[dim].append(merged_coords)
    opts, ents = search_by_query(search_index, query)
    return opts


def search_by_query(search_index, query):
    """
    SEARCH BY QUERY

     excecute filter with search index to query
     #Empty Query {'products': [], 'geography': []}
     #Search indexes = list of all pathes in the tree

    :param search_index:
    :type search_index:
    :param query:
    :type query:
    :return:
    :rtype:
    """
    order = search_index['order']# list of dimensions
    search_indexes = [search_index['direct']] #direct list of pathes
    options = dict()
    entities_ids = []
    query_internal = _transform(query)
    for i, dim_id in enumerate(order):

        # Collect available options.
        keys = []
        for item in search_indexes:
            keys.extend(item.keys())
        # Get current selector.
        dimension_selection = query_internal.get(dim_id)
        # Verify current selector.
        # If selector is empty or not valid set default selector.
        if len(dimension_selection) == 0:
            dimension_selection = sorted(keys)
        else:
            dimension_selection = [x for x in dimension_selection if x in keys]

        options[dim_id] = _fill_options(keys, dimension_selection)
        #fill options
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
                    if search_res in entities_ids:
                        pass
                    else:
                        entities_ids.append(search_res)
        if len(next_iter_indexes) == 0 and i != len(order) - 1:
            raise Exception
        #update status
        search_indexes = next_iter_indexes
    return options, entities_ids


def _search_by_query(search_index, query):

    order = search_index['order']

    reverse = [search_index['direct']]

    keys = [item[1] for item in search_index['reverse'].items()]


    options = {}
    search_index = [dict(data=item[1], num=item[0]) for item in search_index['reverse'].items()]


    selected = search_index
    #iteraction over dimension
    next_iter_indexes = []
    for dim_name in order:
        if query[dim_name] == []:
            selection = selected
        else:
            selection = []
        # fill option for current dimension
        options[dim_name] = __fill_options(keys, [query[dim_name]], dim_name)
        #iteration over value
        print("Options", options)
        for dim_value in query[dim_name]:
            #iteration over selection
            for entity in selected:#selection

                if dim_value in entity['data'][dim_name]:
                    selection.append(entity)
                    next_iter_indexes.append(entity['data'])
                else:
                    pass
        selected = selection
        keys = next_iter_indexes.copy()

    result = [x['num'] for x in selected]
    return options, result


def __fill_options(keys_list, selected_items, dim_name):
    #selected item - selected dimension

    options = dict(
        data=[],
        selected=[JOIN_SYMBOL.join(x) for x in selected_items]
    )


    for item_dict in keys_list:
        item = item_dict[dim_name]
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


def _fill_options(keys_list, selected_items):
    """
    FILL OPTIONS

    SELECTED ITEMS = [('us',), ('uk',)]
        [('italy',), ('mexico',), ('australia',), ('brazil',), ('japan',), ('spain',), ('germany',), ('canada',),
        ('us',), ('uk',)]

    RETURN:
        OPTIONS = {
                    DATA:[NAME:, ID:, PARENT_ID:]
                    SELECTED:[]
                }

    :param keys_list:
    :type keys_list:
    :param selected_items:
    :type selected_items:
    :return:
    :rtype:
    """

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
    """
    #QUERY  = {"DIMENSION NAME": DIMENSION SELECTION/[]}

    #_TRANSFORM => {'DIMENSION NAME': [([dimension_selection])]}
    :param query:
    :type query:
    :return:
    :rtype:
    """
    tuppled_query = dict()
    for dim_name, dim_selection in query.items():
        tuppled_query[dim_name] = \
            [tuple(x.split(JOIN_SYMBOL)) for x in dim_selection]
    return tuppled_query


