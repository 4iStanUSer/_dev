
class Access:
    _data = {}

    def __init__(self, data=None):
        if data is not None:
            self.load(data)

    def load(self, data):
        """
        Proceed and clean(by role features) access data.

        :param data: list of dictionaries
        with 'name'(string) key
        Example:
            [
                {
                    'name': 'new_view_feature'
                },
                {
                    'name': 'new_edit_feature'
                },
                ...
            ]
        :return: True|False
        """
        if data is not None and isinstance(data, list):
            self._data = {}
            for item in data:
                name = item.get('name')
                if name is None:
                    continue
                self._data[name] = True
            return True
        return False

    def save(self):
        """
        Prepare data structure for saving into backup
        :return: [
            {
                'name': 'new_view_feature'
            },
            {
                'name': 'new_edit_feature'
            },
            ...
        ]
        """
        data = [{
                    'name': key
                } for key, value in self._data.items()]
        return data

    def get(self, conf_name):
        return self._data.get(conf_name)
