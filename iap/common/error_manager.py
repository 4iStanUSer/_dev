from pymemcache.client.base import Client
from configparser import ConfigParser
from pyramid import threadlocal
import json

from pyramid.events import ApplicationCreated

import os
# TODO Add implementation (DR)
class ErrorManager:

    def __init__(self):

        self.config = {}
        self.client = Client(('localhost', 11211), serializer=json_serializer,
                deserializer=json_deserializer)
        self.load()
        self.fill_mem_cached()

    def load(self):
        # get active registry
        registry = threadlocal.get_current_registry()
        # get config folder
        config_folder = registry.settings['path.config']
        conf_file = os.path.join(config_folder, "error_manager" + ".ini")
        if os.path.isfile(conf_file):
            parser = ConfigParser()
            parser.read(conf_file, encoding='utf-8')
            data = dict()
            for section in parser.sections():
                data[section] = {}
                for element in parser.items(section):
                    data[section][element[0]] = element[1]
            self.config = data

    def fill_mem_cached(self):
        """

        :return:
        :rtype:

        """
        for error_name in self.config.keys():
            self.client.set(error_name, self.config[error_name])

    def set(self, key, value):
        """

        :param lang:
        :type lang:
        :param ex:
        :type ex:
        :return:
        :rtype:
        """
        self.client.set(key, value)

    def get_lang_ex(self, lang, ex):
        """

        :param lang:
        :type lang:
        :param ex:
        :type ex:
        :return:
        :rtype:
        """
        return self.client.get(ex)[lang]

    def get_error_message(self, lang, ex):
        print(ex)
        error = self.client.get(ex)[lang]
        return error


    def reload(self):
        self.load()


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")