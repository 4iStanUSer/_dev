import memcache
from configparser import ConfigParser
from pyramid import threadlocal
import json

from pyramid.events import ApplicationCreated

import os

class ErrorManager:

    def __init__(self, settings):

        self.config = {}
        self.client = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.load(settings)
        self.fill_mem_cached()

    def load(self, settings):
        # get active registry
        #registry = threadlocal.get_current_registry()
        # get config folder
        config_folder = settings['path.config']
        conf_file = os.path.join(config_folder, "error_manager" + ".ini")
        if os.path.isfile(conf_file):
            parser = ConfigParser()
            parser.read(conf_file, encoding='utf-8')
            data = dict()
            for section in parser.sections():
                data[section] = {}
                for element in parser.items(section):
                    data[section][element[0]] = element[1]
                    print("Data", data)
            self.config = data

    def fill_mem_cached(self):
        """

        :return:
        :rtype:

        """
        for error_name in self.config.keys():
            for lang in self.config[error_name].keys():
                key = "".join([error_name, lang])
                val = self.config[error_name][lang]
                self.client.set(key, val)

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
        key = "".join([ex, lang])
        error = self.client.get(key)
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


def create_error_manager(config):

    settings = config.get_settings()
    em = ErrorManager(settings)

    def get_error_msg(request, lang, error):
        return em.get_error_message(lang, error)

    config.add_request_method(get_error_msg, 'get_error_msg')