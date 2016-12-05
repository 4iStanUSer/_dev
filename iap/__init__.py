import pyramid
from pyramid.config import Configurator
from pyramid.response import Response

from .common import security
from .common.views import common_view as common

from .forecasting.views import dashboard as f_dashboard
from .forecasting.views import default as f_common
from .forecasting.views import scenarios as f_scenarios
from .forecasting.views import simulator as f_simulator


def common_routing(config):
    """
    Configure common routing
    """
    config.add_static_view(name='static', path='iap.ui:dist')
    config.add_static_view(name='images', path='iap.ui:images',
                           cache_max_age=3600)

    #config.add_notfound_view(common.notfound_view)
    #config.add_forbidden_view(common.forbidden_view)

    config.add_route('common.index', '/')
    config.add_view(common.index_view, route_name='common.index')

    config.add_route('common.get_page_configuration',
                     '/get_page_configuration')
    config.add_view(common.get_page_configuration,
                    route_name='common.get_page_configuration',
                    request_method='POST', renderer='json')

    config.add_route('common.get_languages', '/get_languages')
    config.add_view(common.get_languages_list,
                    route_name='common.get_languages',
                    request_method='POST', renderer='json')

    config.add_route('common.set_language', '/set_language')
    config.add_view(common.set_language,
                    route_name='common.set_language',
                    request_method='POST', renderer='json')

    config.add_route('common.get_landing', '/get_landing')
    config.add_view(common.get_landing_page_data,
                    route_name='common.get_landing',
                    request_method='POST', renderer='json')

    config.add_route('common.client_user_view', '/get_client_user_view')
    config.add_view(common.get_client_and_user_info,
                    route_name='common.client_user_view',
                    request_method='POST', renderer='json')

    config.add_route('common.select_project', '/select_project')
    config.add_view(common.set_project_selection,
                    route_name='common.select_project',
                    request_method='POST', renderer='json')

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

    config.add_route('forecast.get_index_page_data',
                     '/get_index_page_data')

    config.add_route('forecast.get_scenarios_list',
                     '/get_scenarios_list')
    config.add_view(f_scenarios.get_scenarios_list,
                    route_name='forecast.get_scenarios_list',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_dashboard_data',
                     '/get_dashboard_data')
    config.add_view(f_dashboard.get_dashboard_data,
                    route_name='forecast.get_dashboard_data',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_cagrs_for_period',
                     '/get_cagrs_for_period')
    config.add_view(f_dashboard.get_cagrs_for_period,
                    route_name='forecast.get_cagrs_for_period',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_decomposition_for_period',
                     '/get_decomposition_for_period')
    config.add_view(f_dashboard.get_decomposition_for_period,
                    route_name='forecast.get_decomposition_for_period',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_options_for_entity_selector',
                     '/get_options_for_entity_selector')
    config.add_view(f_common.get_options_for_entity_selector,
                    route_name='forecast.get_options_for_entity_selector',
                    request_method='POST', renderer='json')



# def wsgi_app(global_config, **settings):
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # TODO learn logging package
    # TODO drink double coffee
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.include('iap.repository.db')
    config.include(common_routing)
    config.include(forecast_routing, route_prefix='/forecast')
    # Add routing for another tools

    return config.make_wsgi_app()
