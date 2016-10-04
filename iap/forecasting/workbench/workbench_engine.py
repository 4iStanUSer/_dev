import copy
import pickle
from .container import Container
from .access import Access
from .dimensions import Dimensions
from .configuration import Configuration

from ...repository.tmp_template import tool_template as tpl  # TODO temp
from ..workbench import helpers

class WorkbenchEngine:
    _storage = {}

    def __init__(self, user_id):
        self._user = user_id
        self.container = Container()
        self.kernel = None
        self.config = Configuration()
        self.access = Access()
        self.dimensions = Dimensions()

        self._wh_inputs = None
        self._wh_outputs = None

    def load_data_from_repository(self, warehouse, i_access, i_man_access):
        root = warehouse.get_root()

        tool_id = 1  # TODO Change this

        u_perms = i_access.get_permissions(tool_id, self._user)
        permissions = u_perms.get('permissions')

        # Fill in access module
        features = [{'name': f.name} for f in u_perms['features']] \
            if u_perms.get('features') is not None else []
        self.access.load(features)

        # Fill in config module
        config = tpl['configuration'] \
            if tpl.get('configuration') is not None else []
        self.config.load(config)

        # Fill in container & dimensions modules
        if root is not None:
            for child in root.children:
                self._go_crawl(child, [child.name], {})

        # TODO - add permissions

    def load(self, backup_):
        # instance = pickle.loads(backup)
        # return True
        backup = pickle.loads(backup_)
        container = backup.get('container') \
            if 'container' in backup else dict()
        config = backup.get('configuration') \
            if 'configuration' in backup else dict()
        access = backup.get('access') \
            if 'access' in backup else dict()
        dimensions = backup.get('dimensions') \
            if 'dimensions' in backup else dict()

        self.container.load(container)
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

        return pickle.dumps({
            'configuration': config,
            'access': access,
            'dimensions': dimensions,
            'container': container
        })

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
        if entity.id not in self.dimensions.entities:
            self.dimensions.entities[entity.id] = {
                'name': entity.name,  # entity
                'id': entity.id
            }

        # TODO REVIEW THIS because it is one-to-many
        # Generate hierarchy
        parent = l_p[dim_name][len(l_p[dim_name]) - 1] \
            if l_p.get(dim_name) and len(l_p[dim_name]) else None
        self.dimensions.dim_ent_hier[dim_name].append({
            'ui_id': entity.id,
            'par_ui_id': parent
        })

        # Parent replacement
        if dim_name not in last_parents:
            last_parents[dim_name] = []
        last_parents[dim_name].append(entity.id)

        # FOR ALL MODULES - Apply method for entity's children
        if entity.children:
            for child in entity.children:
                self._go_crawl(child, path + [child.name], last_parents)

        # FOR DIMENSIONS MODULE
        if len(self.dimensions.dim_list) == len(last_parents):
            key = []
            for dim in self.dimensions.dim_list:
                ind = len(last_parents[dim])-1
                key.append(last_parents[dim][ind])
            self.dimensions.entity_by_path[tuple(key)] = path

        self.dimensions.formatting(self.dimensions.data,
                                   self.dimensions.dim_list,
                                   last_parents)

    def init_container(self, dev_template, wh):
        # Initialize time scales.
        for ts_name, timeline in dev_template['timescales'].items():
            self.container.add_time_scale(ts_name, timeline)
        time_borders = {}
        for ts_name, timeline in dev_template['timescales'].items():
            time_borders[ts_name] = (timeline[0], timeline[-1])
        # Find top entity and run entity init function recursively.
        top_entity_path = dev_template['top_entity']['path']
        wh_ent = wh.get_entity(top_entity_path)
        init_entity(wh_ent, dev_template, time_borders, self.container)
        self.load_data_from_repository()


def init_entity(dev_template, wh_ent, container, input_rules, output_rules):
    cont_ent = container.add_entity(wh_ent.path, wh_ent.path_meta)
    # Find level parameters in developers template.
    level_params = None
    for item in dev_template['structure']:
        meta = helpers.Meta._make(item['meta'])
        if helpers.is_equal_meta(meta, cont_ent.meta):
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
    for item in dev_template['exchange_parameters']:
        meta = helpers.Meta._make(item['meta'])
        if helpers.is_equal_meta(meta, cont_ent.meta):
            exchange_params = item
            break
    if exchange_params is not None:
        inputs_len = len(exchange_params['input_variables'])
        rules = exchange_params['input_variables'] + \
            exchange_params['output_variables']
        for counter, rule in enumerate(rules):
            row = dict(wh_path=wh_ent.path,
                       wh_var=helpers.Variable(rule['wh_var'], rule['wh_ts']),
                       cont_entity_id=cont_ent.id,
                       cont_var=helpers.Variable(rule['cont_var'],
                                                 rule['cont_ts']),
                       time_period=rule['time_period'])
            if counter <= inputs_len:
                input_rules.append(row)
            else:
                output_rules.append(row)
    # Add children
    for child in wh_ent.children:
        init_entity(dev_template, child, container, input_rules, output_rules)


def load_dev_data(dev_template, container):
    for item in dev_template['dev_storage']:
        entity = container.get_entity_by_path(item['path'])
        for name, value in item['coefficients']:
            # TODO add timescale name (DR)
            entity.set_coeff_value(name, '4-4-5', value)


def download_data_from_warehouse_to_container(warehouse, container, mapping):
    # Declare variables.
    wh_entity = None
    cont_entity = None
    prev_wh_entity = None
    prev_cont_entity = None
    for row in mapping:
        # Get warehouse entity is necessary.
        if not helpers.is_equal_path(prev_wh_entity.path,row['wh_path']):
            wh_entity = warehouse.get_entity(row['wh_path'])
            prev_wh_entity = wh_entity
        # Get container entity if necessary.
        if not prev_cont_entity.id == row['cont_entity_id']:
            cont_entity = container.get_entity_by_id(row['cont_entity_id'])
            prev_cont_entity = cont_entity
        # Get data from warehouse.
        wh_var = wh_entity.get_variable(row['wh_var'].var_name)
        wh_ts = wh_var.get_timeseries(row['wh_var'].ts_name)
        values = wh_ts.get_values(row['time_period'])
        # Set data to container.
        cont_var = cont_entity.get_variable(row['cont_var'].var_name)
        cont_ts = cont_var.get_timeseries(row['cont_var'].ts_name)
        cont_ts.set_values(values)

def upload_data_from_container_to_warehouse(warehouse, container, mapping):
    pass
