#from collections import deque

from . import calc_modules

#methodToCall = getattr(foo, 'bar')

class CalculationKernel:
    
    def __init__(self, container):
        self._container = container
        self._queues = {}
        self._buffer = None

    def load_instructions(self, instructions, modules_params):
        for queue_id, queue_content in instructions.items():
            # Add queue.
            # Check for duplicated queues.
            if queue_id in self.queues:
                raise Exception
            curr_queue = Queue()
            self.queues[queue_id] = curr_queue
            # Initialize Modules.
            for calc_mod in queue_content['modules']:
                module_id = calc_mod['id']
                module_type = calc_mod['type']
                # Init module.
                curr_module = getattr(calc_modules, module_type)()
                # Load module parameters.
                curr_module.load_params(modules_parames[queue_id][module_id])
                # Add module to queue's collection.
                curr_queue.add_module(module_id, curr_module)
            # Load input filters.
            for input in queue_content['input']:
                curr_queue.add_inp_filter(input['timescale'], 
                                          input['meta_filter'],
                                          input['variables'])
            # Load output.
            curr_queue.add_output(queue_content['output']['timescale'],
                                  queue_content['output']['meta_filer'],
                                  queue_content['output']['variables'])
            # Load queue scheme.
            for module_id, connections in queue_content['scheme'].items():
                for conn in connections:
                    curr_queue.add_connection(module_id, conn[0], conn[1])

    def init_queue(self):
        # calc buffer size
        # add size of inputs

        
        pass
        #set input buffer size
        # loop modules from queue
        # if there in 0 in input,
        # collect modules to phase 1

class Queue:
    
    def __init__(self):
        self._calc_modules = {}
        self._input_filters = []
        self._output = None
        self._scheme = []
        self._input_size = None
        self._output_mod = None

    def add_module(self, id, module):
        if id in self._calc_modules:
            raise Exception
        self._calc_modules[id] = module

    def add_inp_filter(self, timescale, meta_filter, variables):
        filter = {}
        filter['timescale'] = timescale
        filter['meta'] = {key: list(value) for (key, value) in meta_filter}
        filter['data'] = list(variables)
        self._input_filters.append(filter)

    def add_output(self, timescale, meta_filter, variables):
        self._output['timescale'] = timescale
        self._output['meta'] =\
            {key: list(value) for (key, value) in meta_filter}
        self._output['data'] = list(variables)

    def add_connection(self, mod_id, par_mod_id, pin_index):
        if id not in self._calc_modules:
            raise Exception
        self._scheme[id] = []
        for pin in inp_pins:
            self._scheme[id].append({
                'mod_id': par_mod_id, 
                'pin_ind': pin_index})
'''
    def init(self):
        buffer_size = 0
        buffer_size += self._input_size
        

        while len(sequence) < len(_scheme):
            curr_outup = None
            for out_pin in curr_outup:
                for mod in out_pin:
                    # check if module in sequence
                    # check if module can be added
                    # if yes, add module to tmp collection
                    # and add module  to sequence
            #define new curroutput as 
'''
'''
        curr_depth = 0
        curr_range = range(len(self._scheme))
        while len(curr_range) > 0:
            for i in curr_range:
                z = [item for item in self._scheme[i] if item['mod_id'] == curr_depth]
                if len(z) > 0:

                if self._scheme[i]


        for mod in self._scheme:


        pass


    def _check_scheme_consistency(self):
        pass
        '''
