import copy

from ...common.helper import Meta, Variable
from .helper import SlotType


class DataConfiguration:
    """Describe class here"""

    def __init__(self):

        # Common configuration.
        self._common = dict()
        self._by_meta = dict()
        self._by_entity = dict()

        # Specific settings.
        self._wh_input = []

    def get_backup(self):
        # Save general options.
        project_options = [dict(name=x, value=y) for x, y in
                           self._common.items()]

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
        return dict(project_options=project_options, by_meta=by_meta,
                    by_entities=by_entities, wh_input_long=wh_input)

    def load_from_backup(self, backup):
        self.init_load(backup)

    def init_load(self, config):
        # Fill common configuration.
        for item in config['project_options']:
            self._common[item['name']] = copy.copy(item['value'])

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

    def get_option(self, prop_name, meta=None, entity_path=None):
        try:
            ent_options = self._get_entity_config(meta, entity_path)
            if ent_options is not None:
                prop_val = ent_options.general_options.get(prop_name)
                if prop_val is not None:
                    return prop_val
        except Exception:
            pass
        finally:
            prop_val = self._common.get(prop_name)
            if prop_val is not None:
                return prop_val
            else:
                raise Exception

    def get_view_variables(self, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_view_options('variables')

    def get_view_decomposition(self, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_view_options('decomposition')

    def get_variable_options(self, var_id, lang, meta, entity_path=None):
        ent_options = self._get_entity_config(meta, entity_path)
        if ent_options is None:
            raise Exception
        return ent_options.get_variable_options(var_id, lang)

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
        self.var_properties = dict()
        self.view_options = []
        self.general_options = dict()

    def get_backup(self):
        # Save variables properties.
        variables_properties = []
        for var_id, var_props in self.var_properties.items():
            full_props = copy.copy(var_props)
            full_props['var_id'] = var_id
            variables_properties.append(full_props)

        # Save view options.
        view_options = []
        for item in self.view_options:
            option = []
            meta_options = dict(meta=item['meta'],
                                data=option)
            view_options.append(meta_options)
            for var_opts in item['data']['variables']:
                option.append(dict(
                    var_id=var_opts['id'],
                    view_type=var_opts['type']
                ))
            for var_opts in item['data']['decomposition']:
                option.append(dict(
                    var_id=var_opts['id'],
                    view_type='decomposition',
                    dec_type=var_opts['type']
                ))

        # Save general options.
        general_options = [dict(name=key, value=value) for key, value in
                           self.general_options.items()]

        # Collect backup together.
        return dict(variables_properties=variables_properties,
                    view_options=view_options,
                    general_options=general_options)

    def init_load(self, config):

        # Load variables properties.
        if 'variables_properties' in config:
            for item in config['variables_properties']:
                self.var_properties[item['var_id']] = \
                    {key: copy.copy(value) for key, value in item.items()
                     if key != 'var_id'}

        # Load view options.
        if 'view_options' in config:
            for item in config['view_options']:
                entity_view = dict(variables=[], decomposition=[])
                self.view_options.append(dict(meta=copy.copy(item['meta']),
                                              data=entity_view))
                for var_view in item['data']:
                    view_type = var_view['view_type']
                    if view_type == 'decomposition':
                        d = dict(id=var_view['var_id'],
                                 type=var_view['dec_type'])
                        entity_view['decomposition'].append(d)
                    else:
                        d = dict(id=var_view['var_id'],
                                 type=view_type)
                        entity_view['variables'].append(d)

        # Load general options.
        if 'general_options' in config:
            for item in config['general_options']:
                self.general_options[item['name']] = copy.copy(item['value'])
        return

    def get_view_options(self, view_type):
        result = []
        for option in self.view_options:
            item = dict()
            for var in option['data'][view_type]:
                if var['type'] not in item:
                    item[var['type']] = []
                item[var['type']].append(var['id'])
            if len(item) > 0:
                result.append(dict(meta=option['meta'], data=item))
        return result

    def get_variable_options(self, var_id, lang):
        var_properties = self.var_properties.get(var_id)
        if var_properties is None:
            raise Exception
        if lang not in var_properties['languages']:
            raise Exception
        var_options = copy.copy(var_properties)
        del var_options['languages']
        return {**var_options, **var_properties['languages'][lang]}

