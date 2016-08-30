
class Configuration:
    _data = {}

    def __init__(self, data=None):
        if data is not None:
            self.load(data)

    def load(self, data):
        """
        Proceed configuration data for user.

        :param data: list of dictionaries with 'name' & 'value' keys
        Example:
            [
                {
                    'name': 'dimension_time_widget',
                    'value': 'dropdown'
                },
                {
                    'name': 'cell_bg',
                    'value': '#ccc'
                },
                ...
            ]
        :return: True|False
        """
        self._data = {}
        if data is not None and isinstance(data, list):
            for item in data:
                name = item.get('name')
                if name is not None:
                    self._data[name] = item.get('value')
            return True
        return False

    def save(self):
        """
        Prepare data structure for saving into backup

        :return: list of dictionaries with 'name' & 'value' keys
        Example:
            [
                {
                    'name': 'dimension_time_widget',
                    'value': 'dropdown'
                },
                {
                    'name': 'cell_bg',
                    'value': '#ccc'
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
