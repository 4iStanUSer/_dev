import pyramid
from pyramid.config import Configurator
from pyramid.response import Response

from .common import security
from .common.views import default as common
from .common.views import landing_page as landing
from .forecasting.views import default as forecast
from .ui import temp_routing

def common_routing(config):
    """
    Configure common routing
    """
    config.add_static_view(name='static', path='iap.ui:dist')
    config.add_static_view(name='images', path='iap.ui:images',
                           cache_max_age=3600)

    config.add_notfound_view(common.notfound_view)
    config.add_forbidden_view(common.forbidden_view)

    # http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html#pyramid.config.Configurator.add_tween
    # config.add_tween('.common.tweens.timing_tween_factory', over=pyramid.tweens.MAIN)
    # config.add_tween(common.tweens.login_tween_factory)

    config.add_route('common.index', '/')
    config.add_view(common.index_view, route_name='common.index')

    config.add_route('landing.get_tools_list', '/landing')
    config.add_view(landing.get_tools_list,
                    route_name='landing.get_tools_list',
                    request_method='POST', renderer='json')

    config.add_route('landing.set_tool_selection', '/set_tool_selection')
    config.add_view(landing.set_tool_selection,
                    route_name='landing.set_tool_selection',
                    request_method='POST', renderer='json')

    config.add_route('common.login', '/login')
    config.add_view(common.login_view, route_name='common.login')

    config.add_route('common.logout', '/logout')
    config.add_view(common.logout_view, route_name='common.logout')

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
    config.add_view(forecast.index_view, route_name='forecast.index')

    config.add_route('forecast.get_index_page_data',
                     '/get_index_page_data')
    config.add_view(forecast.get_index_page_data,
                    route_name='forecast.get_index_page_data',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_ui_config',
                     '/get_ui_config')
    config.add_view(forecast.get_ui_config,
                    route_name='forecast.get_ui_config',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_scenarios_list',
                     '/get_scenarios_list')
    config.add_view(forecast.get_scenarios_list,
                    route_name='forecast.get_scenarios_list',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_dashboard_data',
                     '/get_dashboard_data')
    config.add_view(forecast.get_dashboard_data,
                    route_name='forecast.get_dashboard_data',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_cagrs_for_period',
                     '/get_cagrs_for_period')
    config.add_view(forecast.get_cagrs_for_period,
                    route_name='forecast.get_cagrs_for_period',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_decomposition_for_period',
                     '/get_decomposition_for_period')
    config.add_view(forecast.get_decomposition_for_period,
                    route_name='forecast.get_decomposition_for_period',
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
    config.include(temp_routing, route_prefix='/temp')  # TODO Replace: TEMP !!!
    # Add routing for another tools

    return config.make_wsgi_app()
