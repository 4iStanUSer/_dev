from .container import Container


class WorkbenchEngine:

    def __init__(self, user_id):
        self._user = user_id
        self.container = Container()
        self.kernel = None
        self.config = None
        self.access = None

    def load_data_from_repository(self, warehouse):
        pass

    def load_backup(self, backup):
        pass

    def get_data_for_backup(self):
        pass