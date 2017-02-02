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
        """
        Initialisation of workbench
        Args:
            user_id - user identification

        container (Container)- Main Information
        data_config (DataConfiguration)
        calc_kernel (CalculationKernel)
        toll_config (Dict) - dictionary with configuration about tool
        search_index (Dict) - dictionary with parameters
                        order, direct, reverse
        selector (List) - list of selected id's

        :param user_id:
        :type user_id:
        """
        self._user_id = user_id
        self.container = {'default': Container(), 'current': Container()}
        self.data_config = DataConfiguration()
        self.calc_kernel = CalculationKernel()
        self.access = Access()
        self.tool_config = {}
        self.search_index = dict(order=None, direct=None, reverse=None)
        self.selection = []
        self.scenario_selection = []

    def get_backup(self):
        """Get backup of workbench
           in pickle format

        Args:
            Dictionary with
                container_backup
                data_config_backup
                calc_instructions

        :return:
        :rtype:
        """
        container_backup = self.container['current'].get_backup()
        data_config_backup = self.data_config.get_backup()
        calc_instructions = self.calc_kernel.get_backup()

        return pickle.dumps({'container': container_backup, 'data_config': data_config_backup,
                                                        'calc_instructions': calc_instructions})


    def load_from_backup(self, backup_binary, user_access, scenario_id = None):
        """Load from backup

        :param backup_binary:
        :type backup_binary:
        :param user_access:
        :type user_access:
        :return:
        :rtype:
        """

        # Unpickle backup.
        backup = pickle.loads(backup_binary)
        cont_backup = backup.get('container', dict())
        config_backup = backup.get('data_config', dict())
        calc_instructions = backup.get('calc_instructions', dict())
        # Load workbench parts
        if scenario_id == None:
            for container_type in ['default', 'current']:
                self.container[container_type].load_from_backup(cont_backup)
        else:
            self.container["current"].load_from_backup(cont_backup)

        self.data_config.load_from_backup(config_backup)
        self.calc_kernel.load_from_backup(calc_instructions)
        #
        #self.selector = [ent.id for ent in self.container.top_entities]
        # Init wb
        self._init_wb()

    def initial_load(self, warehouse, dev_template, calc_instructions, user_access):
        """
        Initial load

        :param warehouse:
        :type warehouse:
        :param dev_template:
        :type dev_template:
        :param calc_instructions:
        :type calc_instructions:
        :param user_access:
        :type user_access:
        :return:
        :rtype:
        """
        self.data_config.init_load(dev_template)

        for cont_type in ['default', 'current']:
            init_load_service.init_load_container(dev_template, warehouse,
                                                  self.container[cont_type], self.data_config)
            exchange_service.download_data_from_wh(warehouse, self.container[cont_type],
                                                   self.data_config.wh_inputs)

            # Init Calculation kernel.
            self.calc_kernel.load_instructions(calc_instructions)
            # Init wb
            #Init db with user access
            self._init_wb()
            # Run initial calculations.
            calc_service.calculate(self.calc_kernel, self.container[cont_type])

        return

    def _init_wb(self): #input user_access_rights
        """
        Initialise workbench

        Get dimension list from data configuration
        Build search index
        Add selector to WB attr
        :param user_access_rights:
        :type user_access_rights:
        :return:
        :rtype:
        """

        # Build search index.
        dim_names = self.data_config.get_property('dimensions')
        #Build Search Index
        direct_index, reverse_index = \
            dim_service.build_search_index(self.container['default'], dim_names)
        self.search_index['order'] = dim_names
        self.search_index['direct'] = direct_index
        self.search_index['reverse'] = reverse_index

        # Set selector by default.
        empty_query = dim_service.get_empty_query(self.search_index)

        #empty_query = {'products': [], 'products2': [], 'geography': [],'market':["wallmart"]}
        opts, ents = \
            dim_service.search_by_query(self.search_index, empty_query)
        self.selection = ents[5:6]


    def _update_search_index(self, query):
        """
        Update search
        :param query:
        :type query:
        :return:
        :rtype:
        """

        # Init local access manager.
        #for item in user_access_rights:
        #    ent = self.container.get_entity_by_path(item['path'])
        #    if ent is not None:
        #        item['entity_id'] = ent.id
        #self.access.load(user_access_rights, self.container)




