import pickle

from .container import Container
from .access import Access
from .dimensions import Dimensions
from .configuration import Configuration

from .services.loading import init_container
from .services.exchange import download_data_from_wh

class Workbench:

    def __init__(self, user_id):
        self._user_id = user_id
        self.container = Container()
        self.kernel = None
        self.config = Configuration()
        self.access = Access()
        self.dimensions = Dimensions()

        self._wh_inputs = []
        self._wh_outputs = []

    def init_load(self, warehouse, access, dev_template):
        # Access.
        u_perms = access.get_permissions(dev_template['tool_id'], self._user_id)
        permissions = u_perms.get('permissions')
        # Fill in access module
        features = [{'name': f.name} for f in u_perms['features']] \
            if u_perms.get('features') is not None else []
        self.access.load(features)
        # Configuration.
        self.config.load(dev_template.get('configuration', []))
        # Container
        init_container(dev_template, warehouse, self.container,
                       self._wh_inputs, self._wh_outputs)
        download_data_from_wh(warehouse, self.container, self._wh_inputs)
        self.dimensions.build(self.container)

    def load(self, backup_binary):
        backup = pickle.loads(backup_binary)
        # Get data for workbench parts
        container = backup.get('container', dict())
        config = backup.get('configuration', dict())
        access = backup.get('access', dict())
        # Load workbench parts
        self.container.load(container)
        self.config.load(config)
        self.access.load(access)
        # Initialize dimensions tree
        self.dimensions.build(self.container)

    def get_data_for_backup(self):
        container = self.container.save()
        config = self.config.save()
        access = self.access.save()
        return pickle.dumps({
            'configuration': config,
            'access': access,
            'container': container
        })