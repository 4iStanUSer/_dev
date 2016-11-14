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

    def load_instructions(self, instructions):
        # TODO Add description.

        # Load queues
        for q_template in instructions['queues']:
            # Check for duplicated queues.
            if q_template['name'] in self.queues:
                # TODO Define custom exception.
                raise Exception
            # Create new queue and load template.
            queue = Queue()
            queue.load_template(q_template)
            self.queues[q_template['name']] = queue

    def calculate(self, cont, timeline, queue_name, period_ali=None, in_period=None, top_ent=None):
        # TODO Add description.
        # Get queue.
        try:
            queue = self.queues[queue_name]
        except KeyError:
            # TODO Define custom exception.
            raise Exception

        # Define timeline parameters.
        if period_ali is not None:
            period, period_indexes = \
                timeline.get_period_by_alias(queue.inp_ts_name, period_ali)
        else:
            period = in_period
            period_indexes = (timeline.get_index(queue.inp_ts_name, in_period[0]), timeline.get_index(queue.inp_ts_name, in_period[1]))
        time_labels = \
            timeline.get_timeline_by_period(queue.inp_ts_name, period)
        period_len = period_indexes[1] - period_indexes[0] + 1
        last_act, last_act_index = timeline.get_last_actual(queue.inp_ts_name)
        queue.load_timeline_pars(dict(
            last_actual=last_act_index - period_indexes[0] + 1,
            runs_count=period_len))

        # Get entities to run queue for.
        inp_entities = \
            self._get_entities_to_run(cont, queue.input_item_info, top_ent)

        # Loop through entities.
        for entity in inp_entities:

            # Collect coefficients.
            coefficients = []
            for req in queue.coeff_requirements:
                # Get entity.
                curr_ent = self._get_entity_by_filter(cont, entity, req['meta'])
                # Get coefficients.
                for coefficient in req['data']:
                    try:
                        var = curr_ent.get_variable(coefficient[0])
                        coeff = var.get_scalar(queue.inp_ts_name)
                        coefficients.append(coeff.get_value())
                    except Exception:
                        coefficients.append(0)

            # Collect data.
            inputs = []
            for req in queue.inp_requirements:
                # Get entity.
                curr_ent = self._get_entity_by_filter(cont, entity, req['meta'])
                # Get inputs.
                for var_info in req['data']:
                    try:
                        var = curr_ent.get_variable(var_info[0])
                        ts = var.get_time_series(queue.inp_ts_name)
                        values = ts.get_values_for_period(period)
                        inputs.append(values)
                    except Exception:
                        inputs.append([0]*period_len)

            # Prepare queue.
            queue.clean()
            queue.set_constants()
            queue.load_coefficients(coefficients)
            queue.init_modules()

            # Calculation.
            first_out_date = None
            output = []
            tact_counter = 0
            for i in range(period_len):
                queue.set_inputs([x[i] for x in inputs])
                queue.run()
                out = queue.get_output()
                if out is not None:
                    if first_out_date is None:
                        if queue.inp_ts_name != queue.out_ts_name:
                            first_out_date = \
                                timeline.transfer_timescale(time_labels[i],
                                                            queue.inp_ts_name,
                                                            queue.out_ts_name)
                        else:
                            first_out_date = time_labels[i]
                    output.append(out)
                tact_counter += 1
            # Write data to container.
            # TODO find normal approach (DR).
            for ind, item in enumerate(queue.output):
                var_name = item[0]
                slot_type = item[1]
                var = entity.get_variable(var_name)
                if slot_type & 1:
                    ts = var.get_time_series(queue.out_ts_name)
                    ts.set_values_from([x[ind] for x in output],
                                       first_out_date)
                elif slot_type & 4:
                    ps = var.get_periods_series(queue.out_ts_name)
                    ps.set_value(period, output[0][ind])
                else:
                    raise Exception
        return

    def _get_entities_to_run(self, container, input_item_info, top_ent):
        meta_type = input_item_info['type']
        # Exact path to entity. Just get entity.
        if meta_type == FilterType.path:
            path = input_item_info['path']
            return [container.get_entity(path)]
        # Meta filter.
        elif meta_type == FilterType.meta_filter:

            meta_filter = helper_lib.Meta(
                input_item_info['meta_filter'][0],
                input_item_info['meta_filter'][1])

            # Define top entity.
            path = input_item_info.get('top_entity_path')
            if path is not None:
                queue_top_ent = container.get_entity(path)
            else:
                queue_top_ent = None
            top_entity = None #container.get_lower_entity(top_ent, queue_top_ent)
            return container.get_entities_by_meta(meta_filter, top_entity)
        else:
            return []

    def _get_entity_by_filter(self, container, main_ent, ent_filter):
        meta_type = ent_filter['type']
        if meta_type == FilterType.empty:
            res_entity = main_ent
        elif meta_type == FilterType.path:
            res_entity = container.get_entity(ent_filter['path'])
        elif meta_type == FilterType.relative_path:
            res_entity = main_ent.get_child_by_relative_path(ent_filter['path'])
        elif meta_type == FilterType.meta_filter:
            res_entity = \
                main_ent.get_parent_by_meta(
                    helper_lib.Meta(ent_filter['meta_filter'][0],
                                    ent_filter['meta_filter'][1]))
        else:
            raise Exception
        if res_entity is None:
            raise Exception
        return res_entity


class Queue:
    # TODO add description
    def __init__(self):
        # TODO Describe class structure
        self.name = None
        self.input_item_info = None
        self.inp_ts_name = None
        self.out_ts_name = None
        self.coeff_requirements = []
        self.inp_requirements = []

        self.dependents = None
        self.output = None
        #self._calc_modules = {}
        self._calc_instructions = []
        #self._buffer = None
        self._buffer = []
        self._modules_indexes = {}
        self._constants = []
        self._parameters = {}
        self._coeff_refs = []
        self._tl_pars_refs = []
        self._out_indexes = None
        self._out_modules = None
        self._runs_counter = 0

    def load_template(self, template):

        # Read main parameters.
        self.name = template['name']
        self.input_item_info = copy.copy(template['input_item'])
        self.inp_ts_name = template['input_timescale']
        self.out_ts_name = template['output_timescale']
        self.output = [x[0] for x in template['output']]

        # Read data and coefficients
        for item in template['input']:
            if 'coefficients' in item:
                self.coeff_requirements.append(dict(
                    meta=item['meta'], data=item['coefficients']))
                for coeff_info in item['coefficients']:
                    self._coeff_refs.append(dict(par_name=coeff_info[0],
                                                 refs=[]))
            if 'data' in item:
                self.inp_requirements.append(dict(
                    meta=item['meta'], data=item['data']))

        # Read constants.
        if 'constants' in template:
            self._constants.extend(template['constants'])

        # Init structure for timeline parameters references.
        if 'timeline_parameters' in template:
            for item in template['timeline_parameters']:
                self._tl_pars_refs.append(dict(par_name=item, refs=[]))

        # Read modules parameters.
        for mod_id, mod_pars in template['parameters'].items():
            self._parameters[mod_id] = dict()
            for par_name, par_value in mod_pars.items():
                if not isinstance(par_value, tuple):
                    self._parameters[mod_id][par_name] = par_value
                elif par_value[0] == 'coefficients':
                    self._parameters[mod_id][par_name] = None
                    self._coeff_refs[par_value[1]]['refs'].\
                        append(dict(mod_id=mod_id, mod_par_name=par_name))
                elif par_value[0] == 'timeline_parameters':
                    self._parameters[mod_id][par_name] = None
                    self._tl_pars_refs[par_value[1]]['refs'].\
                        append(dict(mod_id=mod_id, mod_par_name=par_name))
                else:
                    raise Exception

        # Set up calculation scheme.
        self._load_scheme(template['modules'], template['input_pins'],
                          [x[1] for x in template['output']])

    def _load_scheme(self, modules, input_pins, output):
        # TODO add description
        # Instantiate modules.
        # Sum out buffer sizes of modules.
        #out_buffer_size = 0
        #for mod_id, mod_type in modules.items():
        #    new_mod = getattr(modeling_library, mod_type)()
        #    out_buffer_size += new_mod.out_size
        #    self._calc_modules[mod_id] = new_mod

        # Collect modules outputs.
        self.dependents = {x: list() for x in modules.keys()}
        self.dependents['inp'] = []
        self.dependents['const'] = []
        for mod_id, pins in input_pins.items():
            for pin in pins:
                if mod_id not in self.dependents[pin[0]]:
                    self.dependents[pin[0]].append(mod_id)

        # Initialize buffer.
        inputs_len = sum([len(x.get('data', [])) for x in self.inp_requirements])
        constants_len = len(self._constants)
        #buffer_size = out_buffer_size + inputs_len + constants_len
        #self._buffer = [0] * buffer_size
        #self._buffer = []
        #buffer_pos = 0

        # Save inputs and constants indexes.
        #self._modules_indexes['inp'] = \
        #    list(range(buffer_pos, buffer_pos + inputs_len))
        #buffer_pos += inputs_len
        #self._modules_indexes['const'] = \
        #    list(range(buffer_pos, buffer_pos + constants_len))
        #buffer_pos += constants_len

        s = len(self._buffer)
        e = inputs_len
        self._buffer.extend([0]*(e))
        self._modules_indexes['inp'] = list(range(s, s + e))

        s = len(self._buffer)
        e = constants_len
        self._buffer.extend([0] * (e))
        self._modules_indexes['const'] = list(range(s, s + e))

        # Define calculation order.
        iter_counter = 0
        prev_output = sorted(self.dependents['inp'] + self.dependents['const'])
        while len(self._calc_instructions) < len(input_pins):
            curr_output = []
            added_flag = False
            for mod_id in prev_output:
                # Check if module already added to calculation queue.
                if mod_id in [x['id'] for x in self._calc_instructions]:
                    continue
                is_ready_to_add = True
                # Check if module dependencies are added to the queue.
                precedents_indexes = []
                for pin in input_pins[mod_id]:
                    inp_mod_id = pin[0]
                    required_flag = pin[2]
                    if required_flag and inp_mod_id not in ['inp', 'const']:
                        try:
                            precedents_indexes.append(
                                [x['id'] for x in self._calc_instructions].index(inp_mod_id)
                            )
                        except ValueError:
                            is_ready_to_add = False
                            break
                # Add module to the queue.
                if is_ready_to_add:
                    added_flag = True
                    new_mod = getattr(modeling_library, modules[mod_id])()
                    self._calc_instructions.append(
                        dict(id=mod_id, module=new_mod, run_result=False,
                             prec_indxs=precedents_indexes)
                    )
                    curr_output.extend(self.dependents[mod_id])
                    # Collect out buffer indexes
                    #start = buffer_pos
                    #end = start + self._calc_modules[mod_id].out_size
                    #self._modules_indexes[mod_id] = list(range(start, end))
                    #buffer_pos += self._calc_modules[mod_id].out_size
                    s = len(self._buffer)
                    e = new_mod.out_size
                    self._buffer.extend([0] * e)
                    self._modules_indexes[mod_id] = list(range(s, s + e))
            # If no modules to add something went wrong.
            if not added_flag:
                # TODO Define custom exception.
                raise Exception
            # Save output of recently added modules for next iteration
            prev_output = sorted(curr_output)
            iter_counter += 1

        # Set input and output buffers for modules.
        #for mod_id, curr_module in self._calc_modules.items():
        #    curr_input = [self._modules_indexes[x[0]][x[1]] for x in input_pins[mod_id]]
        #    curr_output = self._modules_indexes[mod_id]
        #    curr_module.set_input_buffer(self._buffer, curr_input)
        #    curr_module.set_output_buffer(self._buffer, curr_output)
        for item in self._calc_instructions:
            mod_id = item['id']
            curr_module = item['module']
            curr_input = [self._modules_indexes[x[0]][x[1]] for x in input_pins[mod_id]]
            curr_output = self._modules_indexes[mod_id]
            curr_module.set_input_buffer(self._buffer, curr_input)
            curr_module.set_output_buffer(self._buffer, curr_output)


        # Set out indexes
        self._out_indexes = [self._modules_indexes[x[0]][x[1]] for x in output]
        #self._out_modules = [x[0] for x in output]
        ids = [x['id'] for x in self._calc_instructions]

        self._out_modules = [ids.index(x[0]) for x in output if x[0] != 'inp']
        return

    def set_inputs(self, tact_inputs):
        # TODO add description
        inp_indexes = self._modules_indexes['inp']
        for i in range(len(inp_indexes)):
            self._buffer[inp_indexes[i]] = tact_inputs[i]

    def set_constants(self):
        const_indexes = self._modules_indexes['const']
        for i in range(len(const_indexes)):
            self._buffer[const_indexes[i]] = self._constants[i]

    def get_output(self):
        # TODO add description
        #max_delay = max(self._calc_order[x] for x in self._out_modules)
        #s = sum([self._calc_order[x]['run_flag']
        #         for x in self._out_modules if x not in ['inp', 'const']])
        s = sum([self._calc_instructions[x]['run_result'] for x in self._out_modules])
        if len(self._out_modules) == s:
            return [self._buffer[x] for x in self._out_indexes]
        else:
            return None

    def run(self):
        print('\n')
        print('\n')
        print('\n')
        print(self._runs_counter)
        print('\n')
        print('\n')
        print('\n')
        # TODO add description

        for item in self._calc_instructions:
            s = sum([self._calc_instructions[x]['run_result'] for x in item['prec_indxs']])
            if s == len(item['prec_indxs']):
                item['run_result'] = item['module'].run()
                print(item['id'], '      ', item['run_result'])
        #for mod_id, mod_flags in self._calc_order.items():
        #    if not mod_flags['run_permission']:
        #        mod_flags['run_flag'] = False
        #        continue
        #    curr_module = self._calc_modules[mod_id]
        #    run_flag = curr_module.run()
        #    mod_flags['run_flag'] = run_flag
        #    print(mod_id, '      ',run_flag)
        #    for dep_id in self.dependents[mod_id]:
        #        self._calc_order[dep_id]['run_permission'] = run_flag
        self._runs_counter += 1
        return

    def load_coefficients(self, coefficients):
        if len(coefficients) != len(self._coeff_refs):
            raise Exception
        for i in range(len(self._coeff_refs)):
            for ref in self._coeff_refs[i]['refs']:
                self._parameters[ref['mod_id']][ref['mod_par_name']] = \
                    coefficients[i]

    def load_timeline_pars(self, params):
        for item in self._tl_pars_refs:
            if item['par_name'] not in params:
                continue
            for ref in item['refs']:
                self._parameters[ref['mod_id']][ref['mod_par_name']] = \
                    params[item['par_name']]

    def clean(self):
        # Clean buffer.
        if self._buffer is not None:
            for i in range(len(self._buffer)):
                self._buffer[i] = 0
        # Drop runs counter.
        self._runs_counter = 0

    def init_modules(self):
        for item in self._calc_instructions:
            item['module'].clean()
            mod_pars = self._parameters.get(item['id'])
            if mod_pars is not None:
                item['module'].set_parameters(mod_pars)

