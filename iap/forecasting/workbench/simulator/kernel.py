import copy
from enum import Enum
from collections import OrderedDict

from . import modeling_library


class FilterType(Enum):
    empty = 0
    path = 1
    relative_path = 2
    meta_filter = 3


class CalculationKernel:
    # TODO Add description.
    def __init__(self):
        # TODO Describe class structure
        self.queues = {}

    def load_instructions(self, instructions, parameters):
        # TODO Add description.
        for queue in instructions:
            queue_name = queue['name']
            # Check for duplicated queues.
            if queue_name in self.queues:
                # TODO Define custom exception.
                raise Exception
            # Create new queue
            curr_q = Queue()
            # Fill queue parameters
            curr_q.inp_timescale = queue['input_timescale']
            curr_q.out_timescale = queue['output_timescale']
            curr_q.coeff_requirements = copy.copy(queue['coefficients'])
            curr_q.inp_requirements = copy.copy(queue['inputs'])
            self.queues[queue_name] = curr_q
            # Load queue scheme.
            curr_q.load_scheme(queue['scheme'])
            # Load modules' internal parameters
            curr_q.load_parameters(parameters)

    def calculate(self, cont, queue_name, r_top_entity=None,
                  time_period=None):
        # TODO Add description.
        try:
            queue = self.queues[queue_name]
        except KeyError:
            # TODO Define custom exception.
            raise Exception
        # Get entities to run queue for.
        meta_type = queue.input_item_info['type']
        if meta_type == FilterType.path:
            path = queue.input_item_info['path']
            inp_entities = [cont.get_entity(path)]
        elif meta_type == FilterType.meta_filter:
            meta_filter = queue.input_item_info['meta_filter']
            if 'top_entity_path' in queue.input_item_info:
                top_path = queue.input_item_info['top_entity_path']
            else:
                top_path = None
            # Get top entity according to queue parameters
            if top_path is not None:
                q_top_entity = cont.get_entity(top_path)
                if q_top_entity is None:
                    raise Exception
            # Define which entity to use as top entity.
            # Defined by queue parameters or run options.
            if q_top_entity is not None and r_top_entity is not None:
                if not cont.is_single_branch([q_top_entity, r_top_entity]):
                    raise Exception
                if q_top_entity.depth < r_top_entity.depth:
                    top_entity = r_top_entity
                else:
                    top_entity = q_top_entity
            elif q_top_entity is not None:
                top_entity = q_top_entity
            elif r_top_entity is not None:
                top_entity = r_top_entity
            else:
                top_entity = None
            inp_entities = cont.get_entities_by_meta(meta_filter, top_entity)
        # Loop through entities.
        for entity in inp_entities:
            # Collect coefficients.
            coefficients = []
            for req in queue.coeff_requrements:
                # Get entity.
                meta_type = req['meta']['type']
                c_entity = None
                if meta_type == FilterType.empty:
                    c_entity = entity
                elif meta_type == FilterType.path:
                    c_entity = cont.get_entity(req['path'])
                elif meta_type == FilterType.relative_path:
                    c_entity = entity.get_child_by_relative_path(req['path'])
                elif meta_type == FilterType.meta_filter:
                    c_entity = entity.get_parent_by_meta(req['meta_filter'])
                if c_entity is None:
                    raise Exception
                # Get coefficients.
                for name in req['data']:
                    coefficients.append(c_entity.get_coefficient(name))
            # Collect data.
            inputs = []
            for req in queue.inp_requirements:
                # Get entity.
                meta_type = req['meta']['type']
                d_entity = None
                if meta_type == FilterType.empty:
                    d_entity = entity
                elif meta_type == FilterType.path:
                    d_entity = cont.get_entity(req['path'])
                elif meta_type == FilterType.relative_path:
                    d_entity = entity.get_child_by_relative_path(req['path'])
                elif meta_type == FilterType.meta_filter:
                    d_entity = entity.get_parent_by_meta(req['meta_filter'])
                if d_entity is None:
                    raise Exception
                # Get inputs.
                for name in req['data']:
                    var = c_entity.get_variable(name)
                    ts = var.get_time_series(queue.inp_timescale)
                    inputs.append(ts.get_values())
            # Prepare queue.
            queue.clear_buffer()
            queue.clear_modules()
            queue.load_coefficients(coefficients)

            # Calculate number of tacts.
            start, end = cont.timeline.get_period_indexes(queue.inp_timescale,
                                                          time_period)
            ts_adjust = cont.timeline.get_line_divider(queue.inp_timescale,
                                                       queue.out_timescale)
            # Calculation.
            output = []
            tact_counter = 0
            for i in range(start, end):
                tact_counter += 1
                queue.set_inputs([x[tact_counter - 1] for x in inputs])
                queue.run()
                if (tact_counter-1) % ts_adjust == 0:
                    output.append(queue.get_output())
            # Write data to container.
            for ind, var_name in enumerate(queue.output):
                var = entity.get_variable(var_name)
                ts = var.get_time_series(queue.out_timescale)
                ts.set_values('', [x[ind] for x in output])


class Queue:
    # TODO add description
    def __init__(self):
        # TODO Describe class structure
        # Queue parameters, could be moved to kernel class.
        self.input_item_info = None
        self.coeff_requirements = []
        self.inp_requirements = []
        self.inp_timescale = None
        self.out_timescale = None
        # Members necessary for queue functioning.
        self._calc_modules = {}
        self._calc_order = OrderedDict()
        self._coefficients_indexes = {}
        self._buffer = None

#    def add_module(self, mod_id, module):
#        # TODO add description
#        if mod_id in self._calc_modules:
#            # TODO Define custom exception.
#            raise Exception
#        self._calc_modules[mod_id] = module

    def load_scheme(self, scheme):
        # TODO add description
        self._check_scheme_consistency(scheme)
        # Loop through modules to do the following:
        # Instantiate modules.
        # Sum out buffer sizes.
        # Collect modules outputs.
        # Collect modules coefficients indexes.
        out_buffer_size = 0
        modules_outputs = dict.fromkeys(list(scheme['modules'].keys()), [])
        modules_outputs[0] = []
        for module_id, module_info in scheme['modules'].items():
            # Instantiate modules
            curr_module = getattr(modeling_library, module_info['type'])()
            self._calc_modules[module_id] = curr_module
            # Collect modules coefficients indexes.
            if 'coefficients' in module_info:
                self._coefficients_indexes[module_id] = \
                    copy.copy(module_info['coefficients'])
            # Sum out buffer sizes
            out_buffer_size += module_info['out_size']
            # Collect modules outputs
            for pin in module_info['input_pins']:
                if pin[0] == 'inp':
                    index = 0
                else:
                    index = pin[0]
                if module_id not in modules_outputs[index]:
                    modules_outputs[index].append(module_id)
        # Initialize buffer.
        buffer_size = out_buffer_size + scheme['inp_size']
        self._buffer = [0] * buffer_size
        # Add inputs and coefficients to the buffer.
        buffer_pos = 0
        out_indexes = {}
        out_indexes['inp'] = list(range(buffer_pos,
                                        buffer_pos + scheme['inp_size']))
        buffer_pos += scheme['inp_size']
        # Define calculation order.
        prev_output = modules_outputs[0]
        while len(self._calc_order) < len(scheme['modules']):
            curr_output = []
            added_flag = False
            for mod_id in prev_output:
                # Check if module already added to calculation queue.
                if mod_id in self._calc_order:
                    continue
                # Check if module dependencies are added to the queue.
                # Calculate input pins delay.
                is_ready_to_add = True
                pins_delay = []
                input_pins = scheme['modules'][mod_id]['input_pins']
                for inp_pin in input_pins:
                    inp_mod_id = inp_pin[0]
                    required_flag = inp_pin[2]
                    # Check if module dependencies are added to the queue.
                    if (required_flag and inp_mod_id != 'inp'
                            and inp_mod_id not in self._calc_order):
                        is_ready_to_add = False
                        break
                    # Calculate input pins delay.
                    if required_flag:
                        if inp_mod_id == 'inp':
                            delay = 0
                        else:
                            queue_delay = self._calc_order[inp_mod_id]
                            own_delay = self._calc_modules[inp_mod_id].delay
                            delay = queue_delay + own_delay
                        pins_delay.append(delay)
                if is_ready_to_add:
                    added_flag = True
                    self._calc_order[mod_id] = max(pins_delay)
                    curr_output.extend(modules_outputs[mod_id])
                    # Collect out buffer indexes
                    start = buffer_pos
                    out_buff_size = scheme['modules'][str(mod_id)]['out_size']
                    end = start + out_buff_size
                    out_indexes[mod_id] = list(range(start, end))
                    buffer_pos += out_buff_size
            # If no modules to add something went wrong.
            if not added_flag:
                # TODO Define custom exception.
                raise Exception
            # Save output of recently added modules for next iteration
            prev_output = curr_output

        # Set input and output buffers for modules.
        for mod_id, curr_module in self._calc_modules.items():
            curr_input = [out_indexes[x[0]][x[1]]
                          for x in scheme['modules'][mod_id]['input_pins']]
            curr_output = out_indexes[mod_id]
            curr_module.set_input_buffer(self._buffer, curr_input)
            curr_module.set_output_buffer(self._buffer, curr_output)

    def set_inputs(self, tact_inputs):
        # TODO add description
        for i in self._mods_out_indxs[0]:
            self._buffer[i] = tact_inputs[i]

    def get_output(self):
        # TODO add description
        return [self._buffer[x] for x in self._output_indxs]

    def run(self, tact_index):
        # TODO add description
        for mod_id, delay in self._calc_order.items():
            if tact_index >= delay:
                curr_module = self._calc_modules[mod_id]
                curr_module.run()

    def _check_scheme_consistency(self, scheme):
        # TODO add description
        # module id != 0
        pass

    def load_parameters(self, parameters):
        pass

    def load_coefficients(self, coefficients):
        for id, module in self._calc_modules.items():
            if id not in self._coefficients_indexes:
                continue
            values = [coefficients[x] for x in self._coefficients_indexes[id]]
            module.load_parameters(values)

    def clear_buffer(self):
        if self._buffer is not None:
            for item in self._buffer:
                item = 0

    def clear_modules(self):
        for module in self._calc_modules.values():
            module.clean()





