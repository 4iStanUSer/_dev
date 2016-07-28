import pyramid
from pyramid.config import Configurator
from pyramid.response import Response

from . import common
from . import forecasting as forecast


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

    config.add_route('common.login', '/login')
    config.add_view(common.login_view, route_name='common.login')

    config.add_route('common.logout', '/logout')
    config.add_view(common.logout_view, route_name='common.logout')

    config.include('.common.security')


def forecast_routing(config):
    """
    Configure forecasting tool routing
    """
    # config.add_static_view('forecast.static', 'static', cache_max_age=3600)#CONFIGURE

    # http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html#pyramid.config.Configurator.add_view

    # TODO Add redirect
    #context='myproject.resources.Hello', renderer='json' !!!!!!
    config.add_route('forecast.index', '/')
    config.add_view(forecast.index, route_name='forecast.index')

    config.add_route('forecast.get_time_series',
                     '/get_time_series')
    config.add_view(forecast.get_time_series,
                    route_name='forecast.get_time_series',
                    request_method='POST', renderer='json')

    config.add_route('forecast.get_dimension_selector',
                     '/get_dimension_selector')
    config.add_view(forecast.get_dimension_selector,
                    route_name='forecast.get_dimension_selector',
                    request_method='POST', renderer='json')



# def wsgi_app(global_config, **settings):
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # TODO bootstrap pserv via vusual studio
    # TODO learn logging package
    # TODO drink double coffe
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.include(common_routing)
    config.include(forecast_routing, route_prefix='/forecast')
    # Add routing for another tools

    return config.make_wsgi_app()
