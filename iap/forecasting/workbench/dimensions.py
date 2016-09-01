import copy


class Dimensions:
    _dim_list = []
    _entities = {}
    _dim_ent_hier = {}
    _data = {}

    def __init__(self):
        pass

    def get_dimensions(self):
        return self._dim_list

    def save(self):
        return self._data

    def load(self, root):
        self._go_crawl(root, {}, False)  # TODO Question about parent as root

        # TODO maybe sorting?
        return True

    def _go_crawl(self, entity, l_p={}, use_this=True):
        if entity is None:
            return False

        last_parents = copy.deepcopy(l_p)
        # Collect data
        if use_this:
            # Collect dimension
            dim_name = copy.deepcopy(entity._layer)  # ._dimension_name
            dim_name = dim_name.lower()

            if dim_name not in self._dim_list:
                self._dim_list.append(dim_name)
                self._dim_ent_hier[dim_name] = []

            # Collect entities
            if entity._id not in self._entities:
                self._entities[entity._id] = entity

            # TODO REVIEW THIS because it is one-to-many
            # Generate hierarchy
            parent = l_p[dim_name][len(l_p[dim_name]) - 1] \
                if l_p.get(dim_name) and len(l_p[dim_name]) else None
            self._dim_ent_hier[dim_name].append({
                'ui_id': entity._id,
                'par_ui_id': parent
            })

            # Parent replacement
            if dim_name not in last_parents:
                last_parents[dim_name] = []
            last_parents[dim_name].append(entity._id)

        # Go into each child
        if entity.children:
            for child in entity.children:
                self._go_crawl(child, last_parents)

        if use_this:
            self._proc(self._data, self._dim_list, last_parents)

        # # Fill in main table
        # if use_this:
        #     key = []
        #     for d in self._dim_list:
        #         key.append(l_p.get(d))
        #         # key.append(last_parents.get(d))
        #     key = tuple(key)
        #     self._data[key] = entity._id

    def _proc(self, dict_link, dim_list, parents):
        if len(dim_list) > 0:
            d = dim_list[0]
            if d in parents and parents[d] is not None:
                for parent in parents[d]:
                    if parent not in dict_link:
                        dict_link[parent] = {}
                    if len(dim_list) > 1:
                        self._proc(dict_link[parent], dim_list[1:], parents)

    def get_dimension_items(self, dimension, selection):
        """

        :param dimension: string - dimension name
        :param selection: {'geography': 3, 'product': 83}
        :return: list of available Entities or CEntities
        """
        dim_name = dimension.lower()
        if dim_name not in self._dim_list:
            return False

        tmp = self._data
        for dim in self._dim_list:
            if selection.get(dim) is None \
                    or tmp.get(selection[dim]) is None:  # Fail
                return False

            if dim == dim_name:  # Success
                return tmp.keys()  # [self._entities[key] for key in tmp.keys()]

            tmp = tmp[selection[dim]]

    def correct_selection(self, selection):
        pass

    def make_hierarchical(self, dimension, items):
        if dimension not in self._dim_ent_hier:
            return False
        dim_hier = self._dim_ent_hier[dimension]
        plain_dict = {}
        storage = []
        for item in items:
            try:
                self._entities[item]
            except KeyError:
                continue

            # get item
            if item not in plain_dict:
                plain_dict[item] = {
                    'data': self._entities[item],
                    'children': []
                }
            # get item's parents & filter they by items
            parents = [x['par_ui_id'] for x in dim_hier
                       if x['ui_id'] == item and x['par_ui_id'] is not None
                       and x['par_ui_id'] in items]

            if len(parents) > 0:  # create parent -> add into parent
                for parent in parents:
                    if parent not in plain_dict:
                        plain_dict[parent] = {
                            'data': self._entities[parent],
                            'children': []
                        }
                    plain_dict[parent]['children'].append(plain_dict[item])
            else:  # Add into root
                storage.append(plain_dict[item])

        return storage
