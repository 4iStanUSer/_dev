import copy

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

    Return:
        Direct Index {
                        ('mexico',): {('mouthwash',): 13, ('total',): 3}, ('australia',): {('mouthwash',): 20, ('total',): 10},
                        ('uk',): {('mouthwash',): 18, ('total',): 8}, ('us',): {('mouthwash',): 11, ('total',): 1},
                        ('canada',): {('mouthwash',): 12, ('total',): 2}, ('brazil',): {('mouthwash',): 15, ('total',): 5},
                        ('germany',): {('mouthwash',): 14, ('total',): 4}, ('spain',): {('mouthwash',): 16, ('total',): 6},
                        ('japan',): {('mouthwash',): 19, ('total',): 9}, ('italy',): {('mouthwash',): 17, ('total',): 7}
                        }

        Reverse Index {
                        1: {'products': [], 'geography': ['us']},
                        2: {'products': [], 'geography': ['canada']},
                        3: {'products': [], 'geography': ['mexico']},
                        4: {'products': [], 'geography': ['germany']},
                        5: {'products': [], 'geography': ['brazil']},
                        6: {'products': [], 'geography': ['spain']},
                        7: {'products': [], 'geography': ['italy']},
                        8: {'products': [], 'geography': ['uk']},
                        9: {'products': [], 'geography': ['japan']},
                        10: {'products': [], 'geography': ['australia']},
                        11: {'products': ['mouthwash'], 'geography': ['us']},
                        12: {'products': ['mouthwash'], 'geography': ['canada']},
                        13: {'products': ['mouthwash'], 'geography': ['mexico']},
                        14: {'products': ['mouthwash'], 'geography': ['germany']}
                     }

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
            ############################
            if i < len(dim_names) - 1:
                if key not in sub_index:
                    sub_index[key] = dict()
                sub_index = sub_index[key]
            else:
                if key in sub_index:
                    raise Exception
                sub_index[key] = curr_point['node_id']
            ##############################
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
        #get_entity_by_path


def get_options_by_ents(search_index, entities_ids):
    """
    GET OPTIONS BY ENTS

    Attr:

    Entities ids

    Search Index {
        'order':['geography', 'products'],

        'direct': {('mexico',): {('mouthwash',): 13, ('total',): 3},
                    ('australia',): {('mouthwash',): 20, ('total',): 10},
                    ('uk',): {('mouthwash',): 18, ('total',): 8},
                    ('us',): {('mouthwash',): 11, ('total',): 1},
                    ('canada',): {('mouthwash',): 12, ('total',): 2},
                    ('brazil',): {('mouthwash',): 15, ('total',): 5},
                    ('germany',): {('mouthwash',): 14, ('total',): 4},
                    ('spain',): {('mouthwash',): 16, ('total',): 6},
                    ('japan',): {('mouthwash',): 19, ('total',): 9},
                    ('italy',): {('mouthwash',): 17, ('total',): 7}},
        'reverse': {
                    1: {'products': [], 'geography': ['us']},
                    2: {'products': [], 'geography': ['canada']},
                    3: {'products': [], 'geography': ['mexico']},
                    4: {'products': [], 'geography': ['germany']},
                    5: {'products': [], 'geography': ['brazil']},
                    6: {'products': [], 'geography': ['spain']},
                    7: {'products': [], 'geography': ['italy']},
                    8: {'products': [], 'geography': ['uk']},
                    9: {'products': [], 'geography': ['japan']},
                    10: {'products': [], 'geography': ['australia']},
                    11: {'products': ['mouthwash'], 'geography': ['us']},
                    12: {'products': ['mouthwash'], 'geography': ['canada']},
                    13: {'products': ['mouthwash'], 'geography': ['mexico']},
                    14: {'products': ['mouthwash'], 'geography': ['germany']},
                    15: {'products': ['mouthwash'], 'geography': ['brazil']},
                    16: {'products': ['mouthwash'], 'geography': ['spain']},
                    17: {'products': ['mouthwash'], 'geography': ['italy']},
                    18: {'products': ['mouthwash'], 'geography': ['uk']},
                    19: {'products': ['mouthwash'], 'geography': ['japan']},
                    20: {'products': ['mouthwash'], 'geography': ['australia']}}}

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

    # Filter entities by list from input.
    ents_coords = [coords for node_id, coords in reverse_index.items()
                   if node_id in entities_ids]
    #ENTITIES COORDINATES - []

    # Create entity based on coords.
    #QUERY - GET EMPTY QUERY (SERCH INCEX)
    query = get_empty_query(search_index)
    #for entities in ents-coords
    for ent in ents_coords:
        #for dim, coords om ent.items
        for dim, coords in ent.items():
            merged_coords = JOIN_SYMBOL.join(coords)
            if merged_coords not in query[dim]:
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
        """
        Iterate by tuple(number, dimension)
        """
        # Collect available options.
        keys = []
        for item in search_indexes:
            #search_index -?
            keys.extend(item.keys())

        # Get current selection.
        dimension_selection = query_internal.get(dim_id)
        # Verify current selection.
        # If selection is empty or not valid set default selection.
        dimension_selection = [x for x in dimension_selection if x in keys]
        if len(dimension_selection) == 0:
            dimension_selection = [sorted(keys)[0]]

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
                    entities_ids.append(search_res)
        if len(next_iter_indexes) == 0 and i != len(order) - 1:
            raise Exception
        search_indexes = next_iter_indexes
    return options, entities_ids


def _fill_options(keys_list, selected_items):
    """
    FILL OPTIONS

    SELECTED ITEMS = []

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

#QUERY  = {"DIMENSION NAME": DIMENSION SELECTION/[]}
#_TRANSFORM => {'DIMENSION NAME': [([ ])]}

