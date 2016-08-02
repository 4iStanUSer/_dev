from pyramid.renderers import render_to_response
from ..services import getter as getter_service


# TODO Move to common part
def do_success_response(data):
    return {
        'error': False,
        'data': data
    }


def do_error_response(data):
    return {
        'error': True,
        'data': data
    }


def index(req):
    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=req)


def get_index_page_data(req):
    # Get input data
    data = {
        'nav_panel': {
            'order': ['product_dimension', 'region_dimension', 'timeseria_dimension'],
            'dimensions': [
                {
                    'name': 'product_dimension',
                    'widget': 'hierarchy',
                    'data': getter_service.get_hierarchy()
                },
                {
                    'name': 'region_dimension',
                    'widget': 'hierarchy',
                    'data': getter_service.get_hierarchy1()
                },
                {
                    'name': 'timeseria_dimension',
                    'widget': 'dropdown',
                    'data': getter_service.get_dropdown()
                }
            ]
        },
        'content': {
            'order': ['drivers_grid'],
            'zones': [
                {
                    'name': 'drivers_grid',
                    'widget': 'timeseries',
                    'data': getter_service.get_time_series()
                }
            ]
        }
    }
    return do_success_response(data)

