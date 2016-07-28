'''
Module contains main class (engine) for workbench.
'''

import os
import json
from .container import Container
from .simulator import CalculationKernel


class WorkbenchEngine:
    '''
    Class for workbench managing.
    '''

    def __init__(self, user_id):
        self.__user_id = str(user_id) 
        self.__storage_dir = os.path.join(os.path.dirname(__file__),
                                          'storage',self.__user_id)
        if not os.path.exists(self.__storage_dir):
            os.makedirs(self.__storage_dir)
        self.container = Container()
        self.kernel = CalculationKernel(self.container)

    def load_data_from_repository(self):
        #os.path.dirname(__file__) + 
        with open(os.path.dirname('D:\\Projects\\IAP\\Code\\IAP\\test_inputs\\')+'\\test_input.json') as data_file:   
            data = json.load(data_file)
            self.container.setup()
            self.container.load_data_from_rep(data)

    def save_container(self):
        stream = self.container.get_data_for_save()
        file_path = os.path.join(self.__storage_dir, 'cont.pickle')
        with open(file_path, 'wb') as file:
            file.write(stream)

    def load_container(self):
        file_path = os.path.join(self.__storage_dir, 'cont.pickle')
        with open(file_path, 'rb') as file:
            self.container.setup()
            self.container.load_saved_data(file)
    
    def load_kernel(self):
        with open(os.path.dirname('D:\\Projects\\IAP\\Code\\IAP\\test_inputs\\')+'\\test_queue.json') as model_file:   
            model_instructions = json.load(model_file)
            self.kernel.load_model(model_instructions)
        