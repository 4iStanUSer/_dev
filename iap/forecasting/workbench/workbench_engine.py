from .container import Container
from .access import Access
from .dimensions import Dimensions
from .configuration import Configuration

from ...repository import get_wh_interface  # TODO REMOVE


class WorkbenchEngine:
    def __init__(self, user_id, imanage_access, ssn):  # TODO DELETE SSN
        self._user = user_id
        user = imanage_access.get_user(ssn, id=self._user)
        self._user_roles = [x.id for x in user.roles]

        self.loaded = False

        self.container = Container()
        self.kernel = None

        self.config = Configuration()
        self.access = Access(self._user, self._user_roles)
        self.dimensions = Dimensions()

    def load_data_from_repository(self, warehouse):
        pass

    def __get_all_entities(self, entity, path=[], visited=[], cent_list=[]):
        # TODO rework function add parenting somewhere else(not in CEntity method), now adding only one parent
        visited.append(entity)
        centity = self.container.add_entity(path)  # generate path
        entity_var_names = entity.get_variables_names()
        for entity_var_name in entity_var_names:
            entity_var = entity.get_variable(entity_var_name)
            # print('--get_variable--')
            # print(entity_var)
            centity_var = centity.force_variable(entity_var_name, entity_var.default_value)
            ts_names = entity_var.get_time_series_names()
            for ts_name in ts_names:
                ts = entity_var.get_time_series(ts_name)
                # print('--get_ts--')
                # print(ts)
                if ts_name not in self.container.timeline.time_scales:
                    list_of_time_points = ts._time_scale.timeline
                    # print('--list_of_time_points--')
                    # print(list_of_time_points)
                    time_line_list = []
                    for time_point in list_of_time_points:
                        time_line_list.append(time_point.name) #labels
                    self.container.add_time_scale(ts_name, time_line_list)
                centity_ts = centity_var.force_time_series(ts_name, ts._start, ts._end)
                values = ts.get_values()
                # TODO get start label in some other way
                start_label = ts._time_scale.timeline[0].name
                centity_ts.set_values(start_label, values)
        cent_list.append(centity)
        if len(entity.children):
            for child in entity.children:
                if child not in visited:
                    full_path = path + [child.name]
                    self.__get_all_entities(child, full_path, visited, cent_list)
        # TODO remove or replace return value
        return cent_list

    def load_backup(self, backup):  # TODO remove imanage_acc
        self.loaded = True

        config = backup.get('configuration') \
            if 'configuration' in backup else dict()
        access = backup.get('access') \
            if 'access' in backup else dict()
        # dimensions = backup.get('dimensions') \
        #     if 'dimensions' in backup else dict()
        wh = get_wh_interface()

        self.config.load(config)  # TODO clean
        self.access.load(access)  # TODO clean
        self.dimensions.load(wh.get_entity_by_id(1))  # TODO clean

        return True

    def get_data_for_backup(self):
        config = self.config.save()
        access = self.access.save()
        dimensions = self.dimensions.save()

        return {
            'configuration': config,
            'access': access,
            'dimensions': dimensions
        }
