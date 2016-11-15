"""
Describe package here.
"""

import pickle

from .access import Access
from .configuration import Configuration
from .calculation_kernel import CalculationKernel
from .container import Container
from .services.dimensions import build_search_index
from .services.loading import init_configuration, init_container
from .services.exchange import download_data_from_wh
from .services.calculate import calculate
from ...common.calc_instructions import JJOralCare_queue_instructions

class Workbench:

    def __init__(self, user_id):
        self._user_id = user_id
        self.container = Container()
        self.kernel = CalculationKernel()
        self.config = Configuration()
        self.access = Access()
        self.search_index = None
        self._wh_inputs = []
        self._wh_outputs = []

    def load_backup(self, backup_binary):
        backup = pickle.loads(backup_binary)
        # Get data for workbench parts
        container = backup.get('container', dict())
        config = backup.get('configuration', dict())
        access = backup.get('access', dict())
        instructions = backup.get('instructions', dict())
        # Load workbench parts
        self.container.load(container)
        self.config.load(config)
        self.access.load(access)
        self.search_index = build_search_index(self.container,
                                               self.config['dimensions'])
        self.kernel.load_instructions(instructions)
        calculate(self.kernel, self.container)
        
    def get_backup(self):
        container = self.container.save()
        config = self.config.save()
        access = self.access.save()
        return pickle.dumps({
            'configuration': config,
            'access': access,
            'container': container,
            'instructions': JJOralCare_queue_instructions
        })

    def init_load(self, warehouse, dev_template):
        init_configuration(dev_template, self.config)
        init_container(dev_template, warehouse, self.container, self.config,
                       self._wh_inputs, self._wh_outputs)
        download_data_from_wh(warehouse, self.container, self._wh_inputs)
