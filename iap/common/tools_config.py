from configparser import ConfigParser
import os.path
import pyramid.threadlocal as threadlocal

CONF_CONST = 'config'


def get_page_config(tool_id, page_name, language):

    def _read_ini_file(path):
        parser = ConfigParser()
        parser.read(path, encoding='utf-8')
        data = dict()
        for section in parser.sections():
            data[section] = {}
            for element in parser.items(section):
                data[section][element[0]] = element[1]
        return data

    def _merge_and_flatten_configurations(configs):
        final_config = dict()

        for config in configs:
            for section_name, section_content in config.items():
                for par_name, par_value in section_content.items():
                    final_config[section_name + '_' + par_name] = par_value
        return final_config

    registry = threadlocal.get_current_registry()
    config_folder = registry.settings['path.config']
    tool_folder = os.path.join(config_folder, tool_id)
    lang_file = os.path.join(tool_folder, language + '_' + page_name + '.ini')
    conf_file = os.path.join(tool_folder,
                             page_name + '_' + CONF_CONST + '.ini')
    files_names = [lang_file, conf_file]
    configurations = []
    for f_name in files_names:
        if os.path.isfile(f_name):
            configurations.append(_read_ini_file(f_name))
    return _merge_and_flatten_configurations(configurations)


