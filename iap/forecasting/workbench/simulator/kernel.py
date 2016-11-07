import copy
from enum import IntEnum
from collections import OrderedDict
from ....common import helper_lib


from . import modeling_library


class FilterType(IntEnum):
    empty = 0
    path = 1
    relative_path = 2
    meta_filter = 3
    const = 4


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
            curr_q.input_item_info = queue['input_item']
            curr_q.inp_timescale = queue['input_timescale']
            curr_q.out_timescale = queue['output_timescale']
            curr_q.period = queue['period']
            curr_q.output = list(queue['output'])
            curr_q.coeff_requirements = copy.copy(queue['coefficients'])
            curr_q.inp_requirements = copy.copy(queue['inputs'])
            curr_q._constants = list(queue['scheme']['constants'])
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

            q_top_entity = None
            meta_filter = helper_lib.Meta(queue.input_item_info['meta_filter'][0], queue.input_item_info['meta_filter'][1])
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
            for req in queue.coeff_requirements:
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
                elif meta_type == FilterType.const:
                    coefficients.extend(list(req['data']))
                    continue
                if c_entity is None:
                    raise Exception
                # Get coefficients.
                for coef_pair in req['data']:
                    try:
                        value = c_entity.data.get_coeff_value(coef_pair[0], coef_pair[1])
                        coefficients.append(value)
                    except Exception:
                        coefficients.append(0)
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
                    d_entity = entity.get_parent_by_meta(helper_lib.Meta(
                        req['meta']['meta_filter'][0],
                        req['meta']['meta_filter'][1]))
                if d_entity is None:
                    raise Exception
                # Get inputs.
                for name in req['data']:
                    try:
                        values = d_entity.data.get_values(name, queue.inp_timescale, (None, None))
                        inputs.append(values)
                    except Exception:
                        inputs.append([0]*cont.timeline.get_time_length(queue.inp_timescale))
                    #var = d_entity.get_variable(name)
                    #ts = var.get_time_series(queue.inp_timescale)
                    #inputs.append(ts.get_values())
            # Prepare queue.
            queue.clear_buffer()
            queue.drop_counter()
            queue.clean_modules()
            queue.load_coefficients(coefficients)

            # Calculate number of tacts.
            start = cont.timeline.get_index(queue.inp_timescale, queue.period[0])
            end = cont.timeline.get_index(queue.inp_timescale, queue.period[1])
            queue.total_runs_count = end - start + 1

            #ts_adjust = cont.timeline.get_line_divider(queue.inp_timescale,
            #                                           queue.out_timescale)
            ts_adjust = 1
            # Calculation.
            output = []
            tact_counter = 0
            for i in range(start, end + 1):
                queue.set_inputs([x[i] for x in inputs])
                queue.run()
                # (tact_counter-1) % ts_adjust == 0:
                out = queue.get_output()
                if out is not None:
                    output.append(out)
                tact_counter += 1
            # Write data to container.
            for ind, var_name in enumerate(queue.output):
                var = entity.get_variable(var_name)
                ts = var.get_time_series(queue.out_timescale)
                ts.set_values('2016', [x[ind] for x in output])
        return

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
        self.period = None
        self.output = None
        # Members necessary for queue functioning.
        self._calc_modules = {}
        self._calc_order = OrderedDict()
        self._coefficients_indexes = {}
        self._buffer = None

        self._inp_indexes = None
        self._const_indexes = None
        self._out_indexes = None

        self._out_modules = None

        self._runs_counter = 0

        self._constants = None

        self.total_runs_count = 0

    def load_scheme(self, scheme):
        # TODO add description
        self._check_scheme_consistency(scheme)
        # Loop through modules to do the following:
        # Instantiate modules.
        # Sum out buffer sizes.
        # Collect modules outputs.
        # Collect modules coefficients indexes.
        out_buffer_size = 0
        #modules_outputs = dict.fromkeys(list(scheme['modules'].keys()), list())
        modules_outputs = {x: list() for x in scheme['modules'].keys()}
        modules_outputs['inp'] = []
        for module_id, module_info in scheme['modules'].items():
            # Instantiate modules
            self._calc_modules[module_id] = getattr(modeling_library, module_info['type'])(module_info.get('parameters', None))
            # Collect modules coefficients indexes.
            if 'coefficients' in module_info:
                self._coefficients_indexes[module_id] = \
                    copy.copy(module_info['coefficients'])
            # Sum out buffer sizes
            out_buffer_size += module_info['out_size']
            # Collect modules outputs
            for pin in module_info['input_pins']:
                if pin[0] == 'const':
                    continue
                if module_id not in modules_outputs[pin[0]]:
                    modules_outputs[pin[0]].append(module_id)
        # Initialize buffer.
        buffer_size = out_buffer_size + scheme['inp_size'] + len(scheme['constants'])
        self._buffer = [0] * buffer_size
        # Add inputs and constants to the buffer.
        out_indexes = {}
        buffer_pos = 0
        out_indexes['inp'] = list(range(buffer_pos,
                                        buffer_pos + scheme['inp_size']))
        buffer_pos += scheme['inp_size']
        self._inp_indexes = out_indexes['inp']


        const_len = len(scheme['constants'])
        out_indexes['const'] = list(range(buffer_pos,
                                          buffer_pos + const_len))
        self._const_indexes = out_indexes['const']
        buffer_pos += const_len



        # Define calculation order.
        prev_output = modules_outputs['inp']
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
                    if (required_flag and inp_mod_id not in ['inp', 'const']
                            and inp_mod_id not in self._calc_order):
                        is_ready_to_add = False
                        break
                    # Calculate input pins delay.
                    if required_flag:
                        if inp_mod_id in ['inp', 'const']:
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
        # Set out indexes
        self._out_indexes = [out_indexes[x[0]][x[1]] for x in scheme['output']]
        self._out_modules = [x[0] for x in scheme['output']]
        return

    def set_inputs(self, tact_inputs):
        # TODO add description
        for i in range(len(self._inp_indexes)):
            self._buffer[self._inp_indexes[i]] = tact_inputs[i]
        for i in range(len(self._const_indexes)):
            self._buffer[self._const_indexes[i]] = self._constants[i]

    def get_output(self):
        # TODO add description
        max_delay = max(self._calc_order[x] for x in self._out_modules)
        if self._runs_counter > max_delay:
            return [self._buffer[x] for x in self._out_indexes]
        else:
            return None

    def run(self):
        # TODO add description
        for mod_id, delay in self._calc_order.items():
            if self._runs_counter >= delay:
                curr_module = self._calc_modules[mod_id]
                curr_module.run()
        self._runs_counter += 1
        return


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
            module.set_parameters(values)

    def clear_buffer(self):
        if self._buffer is not None:
            for i in range(len(self._buffer)):
                self._buffer[i] = 0

    def clean_modules(self):
        for module in self._calc_modules.values():
            module.clean()

    def drop_counter(self):
        self._runs_counter = 0




