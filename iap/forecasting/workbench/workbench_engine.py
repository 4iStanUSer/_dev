from .container.container import Container, CEntity


class WorkbenchEngine:

    def __init__(self, user_id):
        self._user = user_id
        self.container = Container()
        self.kernel = None
        self.config = None
        self.access = None

    def load_data_from_repository(self, warehouse):
        # TODO rework the following line
        root = warehouse._root
        if root is None:
            return False
        else:
            entities_list = []
            for child_ent in root.children:
                entities_list += self.__get_all_entities(child_ent, [child_ent.name])
            return entities_list

    def __get_all_entities(self, entity, path=[], visited=[], cent_list=[]):
        visited.append(entity)

        centity = self.container.add_entity(path)  # generate path
        entity_var_names = entity.get_variables_names()
        for entity_var_name in entity_var_names:
            entity_var = entity.get_variable(entity_var_name)
            print('--get_variable--')
            print(entity_var)
            centity_var = centity.force_variable(entity_var_name, entity_var.default_value)

            ts_names = entity_var.get_time_series_names()
            for ts_name in ts_names:
                ts = entity_var.get_time_series(ts_name)
                print('--get_ts--')
                print(ts)
                if ts_name not in self.container.timeline.time_scales:
                    list_of_time_points = ts._time_scale.timeline
                    time_line_list = []
                    for time_point in list_of_time_points:
                        time_line_list.append(time_point.timestamp)
                    self.container.add_time_scale(ts_name, time_line_list)
                centity_ts = centity_var.force_time_series(ts_name)
                values = ts.get_values()
                for val in values:
                    print('--get_val--')
                    print(val)
                    # TODO add values
                    # centity_val = centity_ts.set_values(centity_ts.start_point, )


        cent_list.append(centity)
        if len(entity.children):
            for child in entity.children:
                if child not in visited:
                    full_path = path + [child.name]
                    self.__get_all_entities(child, full_path, visited, cent_list)
        return cent_list
        # return visited

    def load_backup(self, backup):
        pass

    def get_data_for_backup(self):
        pass
