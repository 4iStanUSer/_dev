from configparser import ConfigParser
import os.path
import pyramid.threadlocal as threadlocal
from trafaret_config import commandline
import trafaret
import argparse

from iap.common.helper import dicts_merge
CONF_CONST = 'config'

TRAFARET = trafaret.Dict({
    trafaret.Key('dashboard'):
        trafaret.Dict({
            trafaret.Key('default_state'):
                trafaret.Dict({
                    'forecast_timescale': trafaret.String(),
                    'forecast_absolute_rate': trafaret.String(),
                    'forecast_collapse_expand': trafaret.String(),
                    'forecast_active_tab': trafaret.String(),
                    'forecast_tab': trafaret.String(),
                    'decomp_value_volume_price': trafaret.String(),
                    'd_summary_table_collapsed_expanded': trafaret.String(),
                    'd_details_table_collapsed_expanded': trafaret.String(),
                    'd_details_selected_factor': trafaret.Null()
                })
        }),
    trafaret.Key('scenarios'):
        trafaret.Dict({
            trafaret.Key('scenarios'):
            trafaret.Dict({
                'work_list_show_limit': trafaret.Int(),
                'min_search_input_length': trafaret.Int(),
                'sorting_field': trafaret.String(),
                'sorting_order': trafaret.Bool(),
                'dateformat': trafaret.String()
            })
        })
})

TRAFARET_LAN = trafaret.Dict({
    trafaret.Key('landing'):
        trafaret.Dict({
            trafaret.Key('top_menu'):
                trafaret.Dict({
                    'landing': trafaret.String(),
                    'dashboard': trafaret.String(),
                    'comparison': trafaret.String(),
                    'scenarios': trafaret.String(),
                    'simulator': trafaret.String(),
                    'help': trafaret.String()
                }),
            trafaret.Key('logout'):
                trafaret.Dict({
                    'label': trafaret.String()
                })
        }),
    trafaret.Key('dashboard'):
        trafaret.Dict({
            trafaret.Key('selector'):
            trafaret.Dict({
                'items_title': trafaret.String(),
                'search_title': trafaret.String(),
                'search_placeholder': trafaret.String(),
                'search_clear': trafaret.String(),
                'selected_title': trafaret.String(),
                'not_found_items': trafaret.String(),
                'apply_button': trafaret.String(),
                'do_not_proceed': trafaret.String(),
                'cancel_button': trafaret.String()
            }),
            trafaret.Key('general'):
            trafaret.Dict({
                'forecast_block': trafaret.String(),
                'decomposition_block': trafaret.String(),
                'insights_block': trafaret.String(),
                'drivers_summary_block': trafaret.String(),
                'dashboard_tab': trafaret.String(),
                'drivers_summary_tab': trafaret.String(),
                'drivers_details_tab': trafaret.String(),
                'value': trafaret.String(),
                'growth_rate': trafaret.String(),
                'collapse': trafaret.String(),
                'expand': trafaret.String(),
                'explore': trafaret.String(),
                'tab_all': trafaret.String(),
                'absolute': trafaret.String(),
                'growth_cagr': trafaret.String(),
                'driver_contribution': trafaret.String(),
                'driver_change_cagr': trafaret.String(),
                'driver': trafaret.String(),
                'metric': trafaret.String(),
                'cagr': trafaret.String(),
                'sub_drivers_dynamic': trafaret.String(),
                'sub_drivers_impact': trafaret.String(),
                'fact': trafaret.String()
            })

        }),
    trafaret.Key('admin'):
        trafaret.Dict({
            trafaret.Key('admin_tools'):
                trafaret.Dict({
                    'create_user_label': trafaret.String(),
                    'edit_user_label': trafaret.String(),
                    'delete_user_button': trafaret.String(),
                    'reset_user_password_button': trafaret.String(),
                    'add_user_form_button': trafaret.String(),
                    'edit_user_form_button': trafaret.String(),
                    'user_is_not_selected_message': trafaret.String(),
                    'users_list_title': trafaret.String()
                })
        }),
    trafaret.Key('scenarios'):
        trafaret.Dict({
            trafaret.Key('scenarios'):
                trafaret.Dict({
                    'recent_actions_header_name': trafaret.String(),
                    'work_list_header_name': trafaret.String(),
                    'filter_section_name': trafaret.String(),
                    'filter_section_favorites_label': trafaret.String(),
                    'filter_section_shared_label': trafaret.String(),
                    'filter_section_local_label': trafaret.String(),
                    'filter_section_drafts_label': trafaret.String(),
                    'filter_section_final_label': trafaret.String(),
                    'search_input_placeholder': trafaret.String(),
                    'show_multiselect_label': trafaret.String(),
                    'create_new_scenario_label': trafaret.String(),
                    'finalize_scenario_label': trafaret.String(),
                    'share_scenario_label': trafaret.String(),
                    'delete_scenario_label': trafaret.String(),
                    'table_name_row': trafaret.String(),
                    'table_author_row': trafaret.String(),
                    'table_shared_row': trafaret.String(),
                    'table_shared_local_value': trafaret.String(),
                    'table_description_row': trafaret.String(),
                    'table_modified_row': trafaret.String(),
                    'table_status_row': trafaret.String(),
                    'table_worklist_tooltip': trafaret.String(),
                    'table_add_to_favorites_tooltip': trafaret.String(),
                    'table_remove_from_favorites_tooltip': trafaret.String(),
                    'table_copy_tooltip': trafaret.String(),
                    'table_edit_tooltip': trafaret.String(),
                    'table_go_scenario_tooltip': trafaret.String(),
                    'not_found_criteria_scenarios_message': trafaret.String(),
                    'not_found_scenarios_message': trafaret.String()
                })
        })
})


def get_page_config(tool_id, page_name, language):
    """
    Get page configuration for particular tool
    with language specification

    :param tool_id:
    :type tool_id:
    :param page_name:
    :type page_name:
    :param language:
    :type language:
    :return:
    :rtype:
    """
    def _read_ini_file(path):
        """
            Get page configuration from ConfigParser
            Parse .ini file and serialise it to dictionary

        """
        parser = ConfigParser()
        parser.read(path, encoding='utf-8')
        data = dict()
        for section in parser.sections():
            data[section] = {}
            for element in parser.items(section):
                data[section][element[0]] = element[1]
        return data

    def _merge_and_flatten_configurations(configs):
        """
        Transform config in file {section_name + '***' + par_name :par_value}

        :param configs:
        :type configs:
        :return:
        :rtype:
        """
        final_config = dict()

        for config in configs:
            for section_name, section_content in config.items():
                for par_name, par_value in section_content.items():
                    final_config[section_name + '***' + par_name] = par_value
        return final_config
    #get active registry
    registry = threadlocal.get_current_registry()
    #get config folder
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


def get_config(request):
    """
    Get configuration from config.yaml, en_config.yaml

    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype Dict
    """
    ap_config_gen = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap_config_gen, default_config='config/config.yaml')
    options_config_gen = ap_config_gen.parse_args('')
    config_gen = commandline.config_from_options(options_config_gen, TRAFARET)
    # TODO languages from request
    ap_config_lan = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap_config_lan, default_config='config/en_config.yaml')
    options_config_lan = ap_config_lan.parse_args('')
    config_lan = commandline.config_from_options(options_config_lan, TRAFARET_LAN)

    config = dicts_merge(config_gen, config_lan)
    return config
