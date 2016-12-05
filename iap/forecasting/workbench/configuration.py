import copy

from ...common.helper import Meta, Variable
from .helper import SlotType

LANGKEY = 'languages'


class DataConfiguration:
    """Describe class here"""

    def __init__(self):

        # Common configuration.
        self._project_properties = dict()
        self._ts_properties = []
        self._by_meta = dict()
        self._by_entity = dict()

        # Specific settings.
        self._wh_input = []

    def get_backup(self):
        # Save project properties.
        project_props = [dict(name=x, value=y) for x, y in
                           self._project_properties.items()]

        # Save time scales properties.
        ts_props = [x.get_for_save() for x in self._ts_properties]

        # Save config by meta.
        by_meta = []
        for meta, ent_config in self._by_meta.items():
            ent_backup = ent_config.get_backup()
            ent_backup['meta_key'] = [meta.dimension, meta.level]
            by_meta.append(ent_backup)

        # Save entities config.
        by_entities = []
        for ent_path, ent_config in self._by_entity.items():
            ent_backup = ent_config.get_backup()
            ent_backup['path'] = list(ent_path)
            by_entities.append(ent_backup)

        # Save wh inputs.
        wh_input = [dict(
            cont_path=item['cont_path'],
            wh_path=item['wh_path'],
            time_period=item['time_period'],
            cont_var=item['cont_var'].variable,
            cont_ts=item['cont_var'].timescale,
            cont_slot=item['cont_var'].slot,
            wh_var=item['wh_var'].variable,
            wh_ts=item['wh_var'].timescale,
            wh_slot=item['wh_var'].slot
        ) for item in self._wh_input]

        # Collect backup together.
        return dict(
            project_properties=project_props,
            timescales_properties=ts_props,
            by_meta=by_meta,
            by_entities=by_entities,
            wh_input_long=wh_input
        )

    def load_from_backup(self, backup):
        self.init_load(backup)

    def init_load(self, config):
        # Fill project configuration.
        for item in config['project_properties']:
            self._project_properties[item['name']] = copy.copy(item['value'])

        # Fill timescales properties.
        for item in config['timescales_properties']:
            self._ts_properties = [ItemConfig(x)
                                   for x in config['timescales_properties']]

        # Fill config for meta groups.
        for meta_config in config['by_meta']:
            meta_key = Meta(dimension=meta_config['meta_key'][0],
                            level=meta_config['meta_key'][1])
            entity_config = EntityConfiguration()
            entity_config.init_load(meta_config)
            self._by_meta[meta_key] = entity_config

        # Fill entities config.
        for entity_config in config['by_entities']:
            entity_path = tuple(entity_config['path'])
            entity_config = EntityConfiguration()
            entity_config.init_load(entity_config)
            entity_config.path = entity_config['path']
            self._by_entity[entity_path] = entity_config

        # Fill information about wh inputs.
        if 'wh_input' in config:
            for item in config['wh_input']:
                for pair in item['pairs']:
                    for rule in item['rules']:
                        self._wh_input.append(
                            dict(cont_path=pair['cont_path'],
                                 cont_var=Variable(variable=rule['cont_var'],
                                                   timescale=rule['cont_ts'],
                                                   slot=SlotType(
                                                       rule['cont_slot'])),
                                 wh_path=pair['wh_path'],
                                 wh_var=Variable(variable=rule['wh_var'],
                                                 timescale=rule['wh_ts'],
                                                 slot=SlotType(
                                                     rule['wh_slot'])),
                                 time_period=rule['time_period'])
                        )
        elif 'wh_input_long' in config:
            for rule in config['wh_input_long']:
                self._wh_input.append(
                    dict(cont_path=rule['cont_path'],
                         cont_var=Variable(variable=rule['cont_var'],
                                           timescale=rule['cont_ts'],
                                           slot=SlotType(rule['cont_slot'])),
                         wh_path=rule['wh_path'],
                         wh_var=Variable(variable=rule['wh_var'],
                                         timescale=rule['wh_ts'],
                                         slot=SlotType(rule['wh_slot'])),
                         time_period=rule['time_period'])
                )
        return

    def get_property(self, prop_name, meta=None, entity_path=None):
        try:
            ent_options = self._get_entity_config(meta, entity_path)
            if ent_options is not None:
                prop_val = ent_options.general_props.get(prop_name)
                if prop_val is not None:
                    return prop_val
        except Exception:
            pass
        finally:
            prop_val = self._project_properties.get(prop_name)
            if prop_val is not None:
                return prop_val
            else:
                raise Exception

    def get_vars_for_view(self, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_view_vars('variables')

    def get_decomp_vars_for_view(self, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_view_vars('decomposition')

    def get_variables_properties(self, vars_ids, lang, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_vars_props(vars_ids, lang)

    def get_timescales_info(self, ts_ids, lang):
        return [x.get_for_view(lang)
                for x in self._ts_properties if x.id in ts_ids]

    def get_dec_types_info(self, lang, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_dec_types_info(lang)

    def get_factor_drivers_relations(self, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_factor_drivers_relations()

    @property
    def wh_inputs(self):
        return copy.copy(self._wh_input)

    def _get_entity_config(self, meta, entity_path=None):
        if entity_path is not None:
            entity_config = self._by_entity.get(tuple(entity_path))
            if entity_config is not None:
                return entity_config

        return self._by_meta.get(meta)


class EntityConfiguration:

    def __init__(self):
        self.var_props = []
        self.view_vars = []
        self.general_props = dict()
        self.dec_types = []
        self.factor_drivers = dict()

    def get_backup(self):
        # Save view options.
        view_options = []
        for item in self.view_vars:
            option = []
            meta_options = dict(filter=item['filter'],
                                variables=option)
            view_options.append(meta_options)
            for var_opts in item['variables']['variables']:
                option.append(dict(
                    id=var_opts['id'],
                    view_type=var_opts['type']
                ))
            for var_opts in item['variables']['decomposition']:
                option.append(dict(
                    id=var_opts['id'],
                    view_type='decomposition',
                    dec_type=var_opts['type']
                ))

        # Collect backup together.
        return dict(
            view_variables=view_options,
            variables_properties=[x.get_for_save() for x in self.var_props],
            general_properties=[dict(name=key, value=value) for key, value in self.general_props.items()],
            decomposition_types=[x.get_for_save() for x in self.dec_types],
            factor_drivers = copy.copy(self.factor_drivers)
        )

    def init_load(self, config):

        # Load variables properties.
        if 'variables_properties' in config:
            self.var_props = [ItemConfig(x)
                              for x in config['variables_properties']]

        # Load view options.
        if 'view_variables' in config:
            for item in config['view_variables']:
                entity_view = dict(variables=[], decomposition=[])
                self.view_vars.append(dict(filter=copy.copy(item['filter']),
                                           variables=entity_view))
                for var_view in item['variables']:
                    view_type = var_view['view_type']
                    if view_type == 'decomposition':
                        d = dict(id=var_view['id'],
                                 type=var_view['dec_type'])
                        entity_view['decomposition'].append(d)
                    else:
                        d = dict(id=var_view['id'],
                                 type=view_type)
                        entity_view['variables'].append(d)

        # Load dec types.
        if 'decomposition_types' in config:
            self.dec_types = [ItemConfig(x)
                              for x in config['decomposition_types']]

        # Load connections between factors and drivers.
        if 'factor_drivers' in config:
            self.factor_drivers = copy.copy(config['factor_drivers'])

        # Load general options.
        if 'general_properties' in config:
            for item in config['general_properties']:
                self.general_props[item['name']] = copy.copy(item['value'])
        return

    def get_view_vars(self, view_type):
        result = []
        for option in self.view_vars:
            if len(option['variables'][view_type]) > 0:
                result.append(
                    dict(filter=option['filter'],
                         variables=copy.copy(option['variables'][view_type]))
                )
        return result

    def get_vars_props(self, vars_ids, lang):
        return [x.get_for_view(lang)
                for x in self.var_props if x.id in vars_ids]

    def get_dec_types_info(self, lang):
        return [x.get_for_view(lang) for x in self.dec_types if x.id]

    def get_factor_drivers_relations(self):
        return copy.copy(self.factor_drivers)


class ItemConfig:

    def __init__(self, props):
        if 'id' not in props.keys():
            raise Exception
        self.general_props = {x: y for x, y in props.items() if x != LANGKEY}
        if LANGKEY in props:
            self.lang_specific_props = copy.copy(props[LANGKEY])

    @property
    def id(self):
        return self.general_props['id']

    def get_for_view(self, lang):
        return {
            **copy.copy(self.general_props),
            **copy.copy(self.lang_specific_props[lang])
        }

    def get_for_save(self):
        result = copy.copy(self.general_props)
        result[LANGKEY] = copy.copy(self.lang_specific_props)
        return result



