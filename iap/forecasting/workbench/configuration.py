import copy

from ...common.helper import Meta, Variable
from .helper import SlotType

#LANGKEY = 'languages'
LANGKEY = ["lang-en-metric", "lang-ru-metric", "lang-en-short_name",
            "lang-ru-full_name", "lang-ru-short_name", "lang-en-full_name"]


class DataConfiguration:
    """Describe class here"""

    def __init__(self):
        self._general = Config()
        self._by_meta = dict()
        self._by_entity = dict()

    def get_backup(self):
        """
        Get Backup of DataConfiguration
        :return:
        :rtype:
        """
        return dict(
            general=self._general,
            by_meta=self._by_meta,
            by_entity=self._by_entity
        )

    def load_from_backup(self, backup):
        """
        Load from backup

        :param backup:
        :type backup:
        :return:
        :rtype:
        """
        self._general = copy.copy(backup['general'])
        self._by_meta = copy.copy(backup['by_meta'])
        self._by_entity = copy.copy(backup['by_entity'])

    def init_load(self, config):
        """
        Initialise filling DataConfiguration

        :param config:
        :type config:
        :return:
        :rtype:
        """

        # Fill project configuration.
        if 'project_properties' in config:
            self._general.load_properties(config['project_properties'])

        # Fill objects configuration.
        objects_names = [
            'timescale_properties',
            'variable_properties',
            'decomposition_properties',
            'selector_properties'
        ]
        for name in objects_names:
            if name in config:
                last_ind = name.find('properties') - 1
                self._general.load_objects_properties(name[:last_ind], config[name])

        # Fill information about wh inputs.
        if 'wh_inputs' in config:
            self._general.load_wh_inputs(config['wh_inputs'])

        # Fill factors drivers and view properties.
        names = ['factor_drivers', 'view_properties']
        for name in names:
            if name not in config:
                continue
            for item in config[name]:
                if 'filter' in item:
                    meta_key = Meta(dimension=item['filter'][0],
                                    level=item['filter'][1])
                    ent_config = self._by_meta.get(meta_key)
                    if ent_config is None:
                        ent_config = Config()
                        self._by_meta[meta_key] = ent_config
                elif 'path' in item:
                    entity_path = tuple(item['path'])
                    ent_config = self._by_entity.get(entity_path)
                    if ent_config is None:
                        ent_config = Config()
                        ent_config.path = entity_path
                        self._by_entity[entity_path] = ent_config
                else:
                    raise Exception
                if name == 'factor_drivers':
                    ent_config.load_factors_drivers(item)
                elif name == 'view_properties':
                    ent_config.load_view_vars(item)


    def get_property(self, prop_name, **kwargs):
        ent_options = self._get_entity_config(**kwargs)
        prop_val = ent_options.properties.get(prop_name)
        if prop_val is not None:
            return prop_val
        raise Exception

    def get_vars_for_view(self, **kwargs):
        #check is it possible
        #path/meta
        ent_options = self._get_entity_config(**kwargs)
        result = ent_options.get_view_vars('variables')
        if result is not None:
            return result
        raise Exception

    def get_decomp_vars_for_view(self, **kwargs):
        ent_options = self._get_entity_config(**kwargs)
        result = ent_options.get_view_vars('decomposition')
        if result is not None:
            return result
        return []
        #raise Exception

    def get_factor_drivers_relations(self, **kwargs):
        ent_options = self._get_entity_config(**kwargs)
        result = ent_options.get_factor_drivers()
        if result is not None:
            return result
        return dict()
        #raise Exception

    def get_duetons_tree(self, **kwargs):
        ent_options = self._get_entity_config(**kwargs)
        result = ent_options.get_dueton_tree()
        if result is not None:
            return result
        return dict()

    def get_objects_properties(self, object_type, ids, lang, **kwargs):
        """
        Get object Property
         Args:
            object_type
            ids
            lang
            **kwarg
        Example:
            get_objects_properties('selector', dimensions, lang)

            Get Entities Options {}
            From Entities Option get object property

        :param object_type:
        :type object_type:
        :param ids:
        :type ids:
        :param lang:
        :type lang:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ent_options = self._get_entity_config(**kwargs)
        result = ent_options.get_object_property(object_type, ids, lang)

        if result is not None:
            return result
        raise Exception


    @property
    def wh_inputs(self):
        return self._general.get_wh_inputs()

    def _get_entity_config(self, **kwargs):
        if 'path' in kwargs:
            entity_config = self._by_entity.get(tuple(kwargs['path']))
            if entity_config is not None:
                return entity_config
        if 'meta' in kwargs:
            entity_config = self._by_meta.get(kwargs['meta'])
            if entity_config is not None:
                return entity_config
        return self._general


class Config:
    """
    Class configuration
    """
    def __init__(self):
        self.properties = dict()
        #dictionary of properies
        self.objects_properties = dict()
        #dict of obj properies
        self.factors_drivers = dict()
        self.duetons = dict()

        self.view_vars = dict()
        self.wh_inputs = []

    def load_properties(self, props):
        """
        Load Properties

        :param props:
        :type props:
        :return:
        :rtype:

        """
        for item in props:
            self.properties[item['name']] = copy.copy(item['value'])

    def load_objects_properties(self, object_type, props):
        """
        Load Object Properties

        Args: Object Type
              Props

        :param object_type:
        :type object_type:
        :param props:
        :type props:
        :return:
        :rtype:
        """

        self.objects_properties[object_type] = [ItemConfig(x) for x in props]

    def load_view_vars(self, item):
        key = tuple(item['nextfilter'])
        if key not in self.view_vars:
            self.view_vars[key] = dict(variables=[], decomposition=[])
        if item['view_type'] == 'decomposition':
            d = dict(id=item['id'],
                     type=item['dec_type'])
            self.view_vars[key]['decomposition'].append(d)
        else:
            d = dict(id=item['id'],
                     type=item['view_type'])
            self.view_vars[key]['variables'].append(d)
        return

    def load_factors_drivers(self, item):
        if item['main_factor'] not in self.factors_drivers:
            self.factors_drivers[item['main_factor']] = []
        self.factors_drivers[item['main_factor']]\
            .append(tuple([item['factor'], item['driver']]))
        return

    def load_dueton_tree(self, item):
        if item['id'] not in self.duetons.keys():
            self.duetons[item['id']] = []
        self.duetons[item['id']]\
            .append(tuple([item['id'], item['parent_id']]))

    def load_wh_inputs(self, inputs):
        self.wh_inputs = copy.copy(inputs)

    def get_wh_inputs(self):
        return copy.copy(self.wh_inputs)

    def get_view_vars(self, view_type):
        try:
            result = []
            for key, value in self.view_vars.items():

                if len(value[view_type]) > 0:
                    if len(key) == 0:
                        filter = {'type': 0}
                    else:
                        filter = {'type': 3, 'meta_filter': key}

                    result.append(
                        dict(filter=filter,
                             variables=copy.copy(value[view_type]))
                    )
        except KeyError:
            return None
        if len(result) == 0:
            return None
        return result

    def get_factor_drivers(self):
        if len(self.factors_drivers) == 0:
            return None
        return copy.copy(self.factors_drivers)

    def get_dueton_tree(self):
        if len(self.duetons) == 0:
            return None
        return copy.copy(self.duetons)

    def get_object_property(self, object_type, ids, lang):
        obj_props = self.objects_properties.get(object_type)
        if obj_props is None:
            return None
        result = [x.get_for_view(lang) for x in obj_props if x.id in ids]
        if len(result) == 0:
            return None
        return result


class ItemConfig:

    def __init__(self, props):

        self.lang_specific_props = {}
        if 'id' not in props.keys():
            raise Exception
        self.general_props = {x: y for x, y in props.items() if x not in LANGKEY}
        for lang_key in LANGKEY:
            if lang_key in props:
                self.lang_specific_props[lang_key]=copy.copy(props[lang_key])

    @property
    def id(self):
        return self.general_props['id']

    @property
    def lang(self):
        return self.lang_specific_props

    def get_for_view(self, lang):

        lang_spec_prop = self.lang_specific_props
        if self.lang_specific_props == {}:
            return [copy.copy(self.general_props)]

        else:
            lang_extracted = get_lang_spec_prop(lang, lang_spec_prop)
        return [dict(lang_extracted, **copy.copy(self.general_props))]

    def get_for_save(self):

        result = copy.copy(self.general_props)
        result[LANGKEY] = copy.copy(self.lang_specific_props)
        return result



def get_lang_spec_prop(lang,lang_spec_prop):

    lang_extracted = {}

    for key in lang_spec_prop.keys():
        if key.split("-")[1]==lang:
            _key = key.split("-")[-1]
            lang_extracted[_key] = lang_spec_prop[key]

    return lang_extracted