from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('./')

@pytest.fixture
def web_app():
    """
    Fixture for server preparation

    :return:
    :rtype: webtest.app.TestApp
    """
    settings = get_appsettings(os.path.join(ABS_PATH, 'test.ini'), name='main')
    app = main(global_config=None, **settings)
    from webtest import TestApp
    testapp = TestApp(app)
    return testapp

@pytest.fixture
def token(web_app):
    """
    Fixture produce token for authentification

    :param web_app:
    :type web_app: webtest.app.TestApp
    :return:
    :rtype: str
    """

    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {'data': {"username": login, 'password': password}})
    token = str(res.json_body['data'])

    return token


def test_get_config(web_app, token):
    data = web_app.post_json("/get_config", headers={'X-Token': token})
    actual = json.loads(data.json)
    expected = {'landing': {'top_menu': {'help': 'Help', 'dashboard': 'Dashboard',
                                         'scenarios': 'Scenarios', 'simulator': 'Simulator',
                                         'landing': 'Home', 'comparison': 'Comparison'},
                            'logout': {'label': 'Log Out'}},
                'dashboard': {'default_state': {'forecast_collapse_expand': 'collapse',
                                                'd_summary_table_collapsed_expanded': 'expanded',
                                                'forecast_tab': 'all', 'decomp_value_volume_price': 'value',
                                                'd_details_table_collapsed_expanded': 'expanded',
                                                'forecast_absolute_rate': 'absolute', 'forecast_timescale': 'annual',
                                                'forecast_active_tab': 'all', 'd_details_selected_factor': None},
                              'general': {'explore': 'Explore', 'driver_change_cagr': 'Driver Change (CAGR)',
                                          'dashboard_tab': 'Dashboard', 'growth_rate': 'Growth rate',
                                          'collapse': 'Collapse', 'metric': 'Metric', 'value': 'Value',
                                          'drivers_summary_tab': 'Drivers Summary', 'fact': 'Fact',
                                          'drivers_summary_block': 'Drivers Summary',
                                          'sub_drivers_impact': 'Sub-driver\\s impact',
                                          'driver_contribution': 'Driver Contribution to Sales Growth',
                                          'forecast_block': 'Forecast', 'cagr': 'CAGR',
                                          'decomposition_block': 'Decomposition', 'expand': 'Expand',
                                          'insights_block': 'Insights', 'sub_drivers_dynamic': 'Sub-driver\\s dynamic',
                                          'growth_cagr': 'Growth (CAGR)', 'tab_all': 'All', 'absolute': 'Absolute',
                                          'driver': 'Driver', 'drivers_details_tab': 'Driver\\s Details'},
                              'selector': {'selected_title': 'Selected', 'not_found_items': 'Not found items',
                                           'search_title': 'Search',
                                           'do_not_proceed': 'You need to select something to proceed',
                                           'search_clear': 'Clear search', 'search_placeholder': 'Type here',
                                           'items_title': 'Categories', 'cancel_button': 'Cancel',
                                           'apply_button': 'Apply'}},
                'scenarios': {'scenarios': {'table_modified_row': 'Modified', 'filter_section_name': 'Filters',
                                            'filter_section_drafts_label': 'Drafts',
                                            'filter_section_shared_label': 'Shared',
                                            'not_found_criteria_scenarios_message':
                                                'No records found satisfying your criteria',
                                            'dateformat': 'MM.DD.YYYY',
                                            'table_add_to_favorites_tooltip': 'Add to Favorites',
                                            'table_copy_tooltip': 'Copy', 'min_search_input_length': 3,
                                            'table_edit_tooltip': 'Edit', 'table_shared_row': 'Shared',
                                            'table_remove_from_favorites_tooltip': 'Remove from Favorites',
                                            'table_description_row': 'Description',
                                            'work_list_header_name': 'Work List',
                                            'filter_section_local_label': 'Local',
                                            'show_multiselect_label': 'Show multiselect',
                                            'search_input_placeholder': 'Search', 'table_name_row': 'Name',
                                            'table_shared_local_value': 'Local', 'finalize_scenario_label': 'Finalize',
                                            'create_new_scenario_label': 'Create New',
                                            'table_go_scenario_tooltip': 'Go Scenario',
                                            'not_found_scenarios_message': 'Not found scenarios',
                                            'filter_section_favorites_label': 'Favorites',
                                            'table_status_row': 'Status', 'delete_scenario_label': 'Delete',
                                            'filter_section_final_label': 'Final', 'table_author_row': 'Author',
                                            'work_list_show_limit': 5, 'sorting_field': 'name', 'sorting_order': True,
                                            'recent_actions_header_name': 'Recent Actions',
                                            'table_worklist_tooltip': 'Worklist', 'share_scenario_label': 'Share'}},
                'admin': {'admin_tools': {'users_list_title': 'Users List', 'create_user_label': 'Create New User',
                                          'edit_user_form_button': 'Edit User', 'add_user_form_button': 'Create User',
                                          'edit_user_label': 'Show / Edit user', 'delete_user_button': 'Delete User',
                                          'user_is_not_selected_message': 'User is not selected',
                                          'reset_user_password_button': 'Reset Password'}}}
    assert actual == expected