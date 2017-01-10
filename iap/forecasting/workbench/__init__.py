"""
Describe package here.
"""
import pickle
import copy

from .container import Container
from .configuration import DataConfiguration
from .calculation_kernel import CalculationKernel
from .access import Access
from .services import dimensions as dim_service
from .services import initial_load as init_load_service
from .services import exchange as exchange_service
from .services import calculate as calc_service


class Workbench:

    def __init__(self, user_id):
        self._user_id = user_id
        self.container = Container()
        self.data_config = DataConfiguration()
        self.calc_kernel = CalculationKernel()
        self.access = Access()
        self.tool_config = {}
        self.search_index = dict(order=None, direct=None, reverse=None)
        self.selection = []

    def get_backup(self):
        container_backup = self.container.get_backup()
        data_config_backup = self.data_config.get_backup()
        calc_instructions = self.calc_kernel.get_backup()
        return pickle.dumps({
            'container': container_backup,
            'data_config': data_config_backup,
            'calc_instructions': calc_instructions
        })

    def load_from_backup(self, backup_binary, user_access):
        # Unpickle backup.
        backup = pickle.loads(backup_binary)
        cont_backup = backup.get('container', dict())
        config_backup = backup.get('data_config', dict())
        calc_instructions = backup.get('calc_instructions', dict())
        # Load workbench parts
        self.container.load_from_backup(cont_backup)
        self.data_config.load_from_backup(config_backup)
        self.calc_kernel.load_from_backup(calc_instructions)
        # Init wb
        self._init_wb(user_access)

    def initial_load(self, warehouse, dev_template, calc_instructions, user_access):
        self.data_config.init_load(dev_template)
        init_load_service.init_load_container(dev_template, warehouse,
                                                  self.container, self.data_config)
        exchange_service.download_data_from_wh(warehouse, self.container,
                                               self.data_config.wh_inputs)

        # Init Calculation kernel.
        self.calc_kernel.load_instructions(calc_instructions)
        # Init wb
        #Init db with user access
        self._init_wb(user_access)
        # Run initial calculations.
        calc_service.calculate(self.calc_kernel, self.container)
        return

    def _init_wb(self, user_access_rights):
        # Build search index.

        dim_names = self.data_config.get_property('dimensions')
        #Build Search Index
        direct_index, reverse_index = \
            dim_service.build_search_index(self.container, dim_names)

        self.search_index['order'] = dim_names
        self.search_index['direct'] = direct_index
        self.search_index['reverse'] = reverse_index
        print("Search Index", self.search_index)

        # Set selection by default.
        #empty_query = #dim_service.get_empty_query(self.search_index)
        empty_query = {'products': [], 'products2': [], 'geography': [],'market':["wallmart"]}
        opts, ents = \
            dim_service.search_by_query(self.search_index, empty_query)
        print("Opts", opts)
        print("Ents", ents)

        self.selection = ents
        """
        {'products': [], 'geography': []}

        Opts {'products': {'data': [{'id': 'mouthwash', 'name': 'mouthwash', 'parent_id': None}, {'id': 'total', 'name': 'total', 'parent_id': None}], 'selected': ['mouthwash']}, 'geography': {'data': [{'id': 'mexico', 'name': 'mexico', 'parent_id': None}, {'id': 'italy', 'name': 'italy', 'parent_id': None}, {'id': 'germany', 'name': 'germany', 'parent_id': None}, {'id': 'brazil', 'name': 'brazil', 'parent_id': None}, {'id': 'japan', 'name': 'japan', 'parent_id': None}, {'id': 'uk', 'name': 'uk', 'parent_id': None}, {'id': 'canada', 'name': 'canada', 'parent_id': None}, {'id': 'us', 'name': 'us', 'parent_id': None}, {'id': 'spain', 'name': 'spain', 'parent_id': None}, {'id': 'australia', 'name': 'australia', 'parent_id': None}], 'selected': ['australia']}}
Ents [20]
        """


        # Init local access manager.
        #for item in user_access_rights:
        #    ent = self.container.get_entity_by_path(item['path'])
        #    if ent is not None:
        #        item['entity_id'] = ent.id
        self.access.load(user_access_rights,self.container)
