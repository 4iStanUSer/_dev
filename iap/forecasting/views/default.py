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


def index_view(req):
    # service.recreate_db(req)
    # service.fillin_db(req)
    # getter_service.set_permissions_template(req)
    # getter_service.init_user_wb(req, 1, 1)
    # getter_service.update_user_perms(req)
    # u_perms = getter_service.get_permissions(req, 1, 1)

    getter_service.tmp_workbench(req)

    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=req)


def get_index_page_data(req):
    # 1.Get all available dimensions
    # 2.Get types for of widget for each of them
    # 3.Get available content for every dimension (depends
    # on current|default selection) with selection
    # 4.Get available content blocks
    # 5.Get type of each block
    # 6.Get data for content blocks (depends on values in bullet no.3)

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

