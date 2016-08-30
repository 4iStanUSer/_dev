
class Access:
    _data = {}

    def __init__(self, user_id, user_role_ids, data=None):
        self._user = user_id
        self._user_role = set(user_role_ids)

        if data is not None:
            self.load(data)

    def load(self, data):
        """
        Proceed and clean(by role features) access data.

        :param data: list of dictionaries
        with 'name'(string) & 'roles_id'(list) keys
        Example:
            [
                {
                    'name': 'new_view_feature',
                    'roles_id': [1, 2]
                },
                {
                    'name': 'new_edit_feature',
                    'roles_id': [1]
                },
                ...
            ]
        :return: True|False
        """
        self._data = {}
        if data is not None and isinstance(data, list):
            for item in data:
                name = item.get('name')
                if name is None:
                    continue

                roles_id = item.get('roles_id')
                if roles_id is not None:  # and len(roles_id) > 0
                    intersect = set(roles_id).intersection(self._user_role)
                    if not intersect or len(intersect) == 0:
                        continue
                self._data[name] = item.get('value')

            return True
        return False

    def save(self):
        """
        Prepare data structure for saving into backup
        :return: [
            {
                'name': 'new_view_feature',
                'roles_id': [1]
            },
            {
                'name': 'new_edit_feature',
                'roles_id': [1]
            },
            ...
        ]
        """
        data = []
        for key, value in self._data.items():
            data.append({
                'name': key,
                'value': value
            })
        return data

    def get(self, conf_name):
        return self._data.get(conf_name)
