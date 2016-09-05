import copy
import pickle
from .container import Container
from .access import Access
from .dimensions import Dimensions
from .configuration import Configuration


class WorkbenchEngine:
    _storage = {}

    def __init__(self, user_id, user_roles):
        self._user = user_id
        self._user_roles = user_roles

        self.container = Container()
        self.kernel = None
        self.config = Configuration()
        self.access = Access(self._user, self._user_roles)
        self.dimensions = Dimensions()

    def load_data_from_repository(self, warehouse):
        root = warehouse.get_root()
        if root is None:
            return False
        else:
            for child in root.children:
                self._go_crawl(child, [child.name], {})

    def load_backup(self, backup):
        # instance = pickle.loads(backup)
        # return True
        data = backup.get('data') \
            if 'data' in backup else dict()
        config = backup.get('configuration') \
            if 'configuration' in backup else dict()
        access = backup.get('access') \
            if 'access' in backup else dict()
        dimensions = backup.get('dimensions') \
            if 'dimensions' in backup else dict()

        self.container.load(data)
        self.config.load(config)
        self.access.load(access)
        self.dimensions.load(dimensions)

        return True

    def get_data_for_backup(self):
        # return pickle.dumps(self)
        config = self.config.save()
        access = self.access.save()
        dimensions = self.dimensions.save()
        container = self.container.save()

        return {
            'configuration': config,
            'access': access,
            'dimensions': dimensions,
            'container': container
        }

    def _go_crawl(self, entity, path, l_p):
        # TODO rework function add parenting somewhere
        # else(not in CEntity method), now adding only one parent

        # FOR CONTAINER MODULE:
        # Define centity
        if entity.id not in self._storage:
            centity = self.container.add_entity(path)
            self._storage[entity.id] = centity
        else:
            centity = self._storage[entity.id]

        # Add entity's variables into centity
        ent_var_names = entity.get_variables_names()
        for ent_var_name in ent_var_names:
            # Define variable & add it into centity
            ent_var = entity.get_variable(ent_var_name)
            centity_var = centity.force_variable(ent_var_name,
                                                 ent_var.default_value)

            # Define time series for variable & add them into centity's var
            ts_names = ent_var.get_time_series_names()
            for ts_name in ts_names:
                ts = ent_var.get_time_series(ts_name)

                # Add time scale into container
                if ts_name not in self.container.timeline.time_scales:
                    time_points = ts.get_timeline()
                    time_line = [x.name for x in time_points]
                    self.container.add_time_scale(ts_name, time_line)

                centity_ts = centity_var.force_time_series(ts_name,
                                                           ts.start_point,
                                                           ts.end_point)

                # Define values for time series & add them into centity
                values = ts.get_values()
                start_label = self.container.timeline.\
                    get_label_by_index(ts_name, 0)
                centity_ts.set_values(start_label, values)

        # FOR DIMENSIONS MODULE:
        last_parents = copy.deepcopy(l_p)
        # Collect dimension
        dim_name = copy.deepcopy(entity.layer)  # .dimension
        dim_name = dim_name.lower()

        if dim_name not in self.dimensions.dim_list:
            self.dimensions.dim_list.append(dim_name)
            self.dimensions.dim_ent_hier[dim_name] = []

        # Collect entities
        if entity._id not in self.dimensions.entities:
            self.dimensions.entities[entity._id] = {
                'name': entity.name  # entity
            }

        # TODO REVIEW THIS because it is one-to-many
        # Generate hierarchy
        parent = l_p[dim_name][len(l_p[dim_name]) - 1] \
            if l_p.get(dim_name) and len(l_p[dim_name]) else None
        self.dimensions.dim_ent_hier[dim_name].append({
            'ui_id': entity._id,
            'par_ui_id': parent
        })

        # Parent replacement
        if dim_name not in last_parents:
            last_parents[dim_name] = []
        last_parents[dim_name].append(entity._id)

        # FOR ALL MODULES - Apply method for entity's children
        if entity.children:
            for child in entity.children:
                self._go_crawl(child, path + [child.name], last_parents)

        # FOR DIMENSIONS MODULE
        self.dimensions.formatting(self.dimensions.data,
                                   self.dimensions.dim_list,
                                   last_parents)
