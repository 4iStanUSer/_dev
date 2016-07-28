from .base import BaseCalculationModule

class CMSum:
    pass

 
class CMMultiple:
    pass 


class CMDivide:
    pass

class CMAggregator(BaseCalculationModule):
    
    def __init__(self):
        self.__delay = 0
        self.__input = None
        self.__output = None

    @property
    def delay(self):
        return self.__delay
    
    def run(self):
        raise NotImplementedError

    def set_input(self, buffer):
        raise NotImplementedError

    def set_output(self, buffer):
        raise NotImplementedError

    def load_saved_parameters(self, data_stream):
        raise NotImplementedError

    def get_parameters_for_save(self):
        raise NotImplementedError