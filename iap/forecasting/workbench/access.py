

from .container.cont_interface import Container

#load_user_rights(user_access_rights)
class Access:
    """Class for checking user access_managers"""

    _features = None
    entities = {}
    #sctructure = {"features":[], "entities":[{'path_e':[], "path_c":[], "name":[],"mask":[], "node_type":[]}]}
    def load(self, permissions: dict, container: Container):
        self._features = permissions['features']
        #get features
        permissions_data = permissions['entities']
        #get permissions data

        # sort by paths for correct nesting
        permissions_data.sort(key=lambda data: len(data['path_c']))

        # format data to tree
        for element in permissions_data:

            entity_id = container.get_entity_by_path(element['path_e'])
            entity_key = 'entity_id_{}'.format(entity_id.id)
            if element['node_type'] == 'ent':
                self.entities[entity_key] = {
                    'name': element['name'],
                    'mask': element['mask'],
                    'vars': []
                }
            elif element['node_type'] == 'var':
                self.entities[entity_key]['vars'].append({
                    'name': element['name'],
                    'mask': element.get('mask', self.entities[entity_key]['mask']),
                    'ts': {}
                })
            else:
                for var in self.entities[entity_key]['vars']:
                    if var['name'] == element['path_c'][0]:
                        if element['node_type'] == 'ts':
                            var['ts'] = {
                                'name': element['name'],
                                'tp': {},
                                'mask': element.get('mask', var['mask'])
                            }
                        elif element['node_type'] == 'tp':
                            var['ts']['tp'][element['name']] = element.get('mask', var['ts']['mask'])

    def get_var_access(self, entity_id: id, var_name: str, time_scale: str) -> int:
        """Checking for particular entity"""

        for var in self.entities['entity_id_{}'.format(entity_id)]['vars']:
            if var['name'] == var_name:
                return var['ts']['tp'][time_scale]

    def check_feature_availability(self, feature_name: str) -> bool:
        """Checking rights for feature"""
        return feature_name in [features['name'] for features in self._features]
