
class Dimensions:
    _dim_list = []
    _entities = {}
    _dim_ent_hier = {}

    _last_parent = {}

    data = None

    def __init__(self, data=None):
        if data is not None:
            self.load(data)

    def save(self):
        return self.data

    def load(self, root):
        self._go_crawl(root, {}, False)

    def _go_crawl(self, entity, last_parents={}, use_this=True):
        if entity is None:
            return False

        # Collect data
        if use_this:
            # Collect dimension
            dim_name = entity._dimension_name
            if dim_name not in self._dim_list:
                self._dim_list.append(dim_name)
                self._dim_ent_hier[dim_name] = []

            # Collect entities
            if entity._id not in self._entities:
                self._entities[entity._id] = entity

            # TODO REVIEW THIS because here is one-to-many
            # Generate hierarchy
            self._dim_ent_hier.append({
                'ui_id': entity._id,
                'par_ui_id': last_parents.get(dim_name)
            })

            # Parent replacement
            last_parents[dim_name] = entity._id

        # Go into each child
        if len(entity.children):
            for child in entity.children:
                self._go_crawl(child, last_parents)
