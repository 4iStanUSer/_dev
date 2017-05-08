import pyramid

from pyramid.config import Configurator
from pyramid.response import Response

from .common import security
from .common.security import set_manager
from .common.error_manager import create_error_manager
from .common.views import common_view as common_views
from .common.views import admin_manager as common_admin

from .forecasting.views import dashboard as f_dashboard
from .forecasting.views import common as f_common
from .forecasting.views import scenarios as f_scenarios
from .forecasting.views import simulator as f_simulator
from .forecasting.views import reporting as f_reporting


def common_routing(config):
    """
    Configure common routing
    """
    config.add_static_view(name='static', path='iap.ui:dist')
    config.add_static_view(name='images', path='iap.ui:images',
                           cache_max_age=3600)


    config.add_route('common_views.index', '/')
    config.add_view(common_views.index_view,
                    route_name='common_views.index')

    config.add_route('common_views.get_routing_config', '/routing_config')
    config.add_view(common_views.get_routing_config,
                    route_name='common_views.get_routing_config',
                    renderer='json')

    config.add_route('common_views.check_logged_in', '/check_auth')
    config.add_view(common_views.check_logged_in,
                    route_name='common_views.check_logged_in',
                    renderer='json')

    config.add_route('common_views.login', '/login')
    config.add_view(common_views.login,
                    route_name='common_views.login',
                    renderer='json')

    config.add_route('common_views.logout', 'logout')
    config.add_view(common_views.logout,
                    route_name='common_views.logout',
                    renderer='json')

    config.add_route('common_views.get_page_configuration',
                     '/get_page_configuration')
    config.add_view(common_views.get_page_configuration,
                    route_name='common_views.get_page_configuration',
                    renderer='json')

    config.add_route('common_views.get_config',
                     '/get_config')
    config.add_view(common_views.get_config,
                    route_name='common_views.get_config',
                    renderer='json')

    config.add_route('common_views.get_data_for_header', '/get_header_data')
    config.add_view(common_views.get_data_for_header,
                    route_name='common_views.get_data_for_header',
                    renderer='json')

    config.add_route('common_views.set_language', '/set_language')
    config.add_view(common_views.set_language,
                    route_name='common_views.set_language',
                    renderer='json')

    config.add_route('common_views.get_tools_with_projects',
                     '/get_tools_with_projects')
    config.add_view(common_views.get_tools_with_projects,
                    route_name='common_views.get_tools_with_projects',
                    renderer='json')

    config.add_route('common_views.select_project', '/select_project')
    config.add_view(common_views.set_project_selection,
                    route_name='common_views.select_project',
                    renderer='json')

    config.add_route("common_views.process_data", '/process_data')
    config.add_view(common_views.process_data,
                    route_name="common_views.process_data",
                    renderer="json"
                    )
    """
    Admin manager Routing

    """
    config.add_route('common_views.get_users', '/get_users')
    config.add_view(common_admin.get_users, route_name='common_views.get_users', renderer='json')

    config.add_route('common_views.get_user_details', '/get_user_details')
    config.add_view(common_admin.get_user_details, route_name='common_views.get_user_details', renderer='json')

    config.add_route('common_views.reset_password', '/reset_password')
    config.add_view(common_admin.reset_password, route_name='common_views.reset_password', renderer='json')

    config.add_route('common_views.add_user', '/add_user')
    config.add_view(common_admin.add_user, route_name='common_views.add_user', renderer='json')

    config.add_route('common_views.edit_user', '/edit_user')
    config.add_view(common_admin.edit_user, route_name='common_views.edit_user', renderer='json')

    #config.set_authorization_policy(ACLAuthorizationPolicy())
    #config.set_authorization_policy(AccessManager())
    config.add_directive('set_manager', set_manager)
    config.set_manager()
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret', http_header='X-Token')
    config.include(security)


def forecast_routing(config):
    """
    Configure forecasting tool routing
    """
    # config.add_static_view('forecast.static', 'static', cache_max_age=3600)#CONFIGURE

    # http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html#pyramid.config.Configurator.add_view

    # TODO Add redirect
    #context='myproject.resources.Hello', renderer='json' !!!!!!
    config.add_route('forecast.index', '/')
    config.add_view(f_common.index_view, route_name='forecast.index')

    config.add_route('forecast.get_index_page_data', '/get_index_page_data')

    """
    Scenario Routing

    """
    config.add_route('forecast.create_scenario', '/create_scenario')
    config.add_view(f_scenarios.create_scenario,
                    route_name='forecast.create_scenario', renderer='json')

    config.add_route('forecast.get_scenario_page', '/get_scenario_page')
    config.add_view(f_scenarios.get_scenario_page,
                    route_name='forecast.get_scenario_page', renderer='json')

    config.add_route('forecast.search_and_view_scenario',
                     '/search_and_view_scenario')
    config.add_view(f_scenarios.search_and_view_scenario,
                    route_name='forecast.search_and_view_scenario', renderer='json')

    config.add_route('forecast.get_scenario_details', '/get_scenario_details')
    config.add_view(f_scenarios.get_scenario_details,
                    route_name='forecast.get_scenario_details', renderer='json')

    config.add_route('forecast.change_scenario_name', '/change_scenario_name')
    config.add_view(f_scenarios.change_scenario_name,
                    route_name='forecast.change_scenario_name', renderer='json')

    config.add_route('forecast.mark_as_final',
                     '/mark_as_final')
    config.add_view(f_scenarios.mark_as_final,
                    route_name='forecast.mark_as_final', renderer='json')

    config.add_route('forecast.set_scenario_location',
                     '/set_scenario_location')
    config.add_view(f_scenarios.mark_as_final,
                    route_name='forecast.set_scenario_location', renderer='json')

    config.add_route('forecast.edit_scenario',
                     '/edit_scenario')
    config.add_view(f_scenarios.edit_scenario,
                    route_name='forecast.edit_scenario', renderer='json')

    config.add_route('forecast.include_scenario', '/include_scenario')
    config.add_view(f_scenarios.include_scenario,
                    route_name='forecast.include_scenario', renderer='json')

    config.add_route('forecast.copy_scenario', '/copy_scenario')
    config.add_view(f_scenarios.copy_scenario,
                    route_name='forecast.copy_scenario', renderer='json')

    config.add_route('forecast.get_scenarios_list',
                     '/get_scenarios_list')
    config.add_view(f_scenarios.get_scenarios_list,
                    route_name='forecast.get_scenarios_list', renderer='json')

    config.add_route('forecast.delete_scenario',
                     '/delete_scenario')
    config.add_view(f_scenarios.delete_scenario,
                    route_name='forecast.delete_scenario', renderer='json')

    """
    Dashboard routing
    """
    config.add_route('forecast.get_dashboard_data',
                     '/get_dashboard_data')
    config.add_view(f_dashboard.get_dashboard_data,
                    route_name='forecast.get_dashboard_data', renderer='json')

    config.add_route('forecast.get_cagrs_for_period', '/get_cagrs_for_period')
    config.add_view(f_dashboard.get_cagrs_for_period, route_name='forecast.get_cagrs_for_period', renderer='json')

    config.add_route('forecast.get_decomposition_for_period', '/get_decomposition_for_period')
    config.add_view(f_dashboard.get_decomposition_for_period, route_name='forecast.get_decomposition_for_period',
                    renderer='json')

    """
    Common routing
    """
    config.add_route('forecast.get_options_for_entity_selector', '/get_options_for_entity_selector')
    config.add_view(f_common.get_options_for_entity_selector, route_name='forecast.get_options_for_entity_selector',
                    renderer='json')

    config.add_route('forecast.set_entity_selection', '/set_entity_selection')
    config.add_view(f_common.set_entity_selection, route_name='forecast.set_entity_selection', renderer='json')

    config.add_route('forecast.get_entity_selectors_config', '/get_entity_selectors_config')
    config.add_view(f_common.get_entity_selectors_config, route_name='forecast.get_entity_selectors_config', renderer='json')

    config.add_route('forecast.get_selectors_static_config', '/get_selectors_static_config')
    config.add_view(f_common.get_selectors_static_config, route_name='forecast.get_selectors_static_config', renderer='json')

    """
    Simulator routing
    """
    config.add_route('forecast.set_values', '/set_values')
    config.add_view(f_simulator.set_values, route_name='forecast.set_values', renderer='json')

    config.add_route('forecast.load_scenario', '/load_scenario')
    config.add_view(f_simulator.load_scenario, route_name='forecast.load_scenario', renderer='json')

    config.add_route('forecast.save_scenario', '/save_scenario')
    config.add_view(f_simulator.save_scenario, route_name='forecast.save_scenario', renderer='json')

    config.add_route('forecast.get_simulator_page_data', '/get_simulator_page_data')
    config.add_view(f_simulator.get_simulator_page_data, route_name='forecast.get_simulator_page_data', renderer='json')


    config.add_route('forecast.get_simulator_decomposition', '/get_simulator_decomposition')
    config.add_view(f_simulator.get_simulator_decomposition, route_name='forecast.get_simulator_decomposition',
                    renderer='json')

    config.add_route('forecast.get_simulator_custom_data', '/get_custom_data')
    config.add_view(f_simulator.get_simulator_custom_data, route_name='forecast.get_simulator_custom_data',
                                                            renderer='json')

    """
    Reporting routing
    """
    config.add_route('forecast.get_report_options', '/get_report_options')
    config.add_view(f_reporting.get_report_options,
                    route_name='forecast.get_report_options', renderer='json')
    config.add_route('forecast.generate_report', '/generate_report')
    config.add_view(f_reporting.generate_report,
                    route_name='forecast.generate_report', renderer='json')


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # TODO learn logging package
    # TODO drink double coffee
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.include('iap.common.repository.db')
    config.include(common_routing)
    config.include(forecast_routing, route_prefix='/forecast')

    # Add routing for another tools

    config.add_directive('create_error_manager', create_error_manager)
    config.create_error_manager()

    return config.make_wsgi_app()
