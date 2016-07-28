from abc import ABCMeta, abstractmethod, abstractproperty

class BaseCalculationModule(metaclass=ABCMeta): 
    
    @abstractproperty
    def delay(self):
        ''' ttt '''
        raise NotImplementedError
    
    @abstractmethod
    def run(self):
        ''' ttt '''
        raise NotImplementedError

    @abstractmethod
    def set_input(self, buffer):
        ''' ttt '''
        raise NotImplementedError

    @abstractmethod
    def set_output(self, buffer):
        ''' ttt '''
        raise NotImplementedError

    @abstractmethod
    def load_saved_parameters(self, data_stream):
        ''' ttt '''
        raise NotImplementedError

    @abstractmethod
    def get_parameters_for_save(self):
        ''' ttt '''
        raise NotImplementedError