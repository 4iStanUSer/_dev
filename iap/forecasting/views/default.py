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


def get_time_series(req):
    return do_success_response(getter_service.get_time_series())


def get_dimension_selector(req):
    if not req.json.get('dimension') or \
                    req.json.get('dimension') not in ['one', 'two']:
        return do_error_response('Wrong dimension')

    if req.json.get('dimension') == 'one':
        data = getter_service.get_hierarchy()
    elif req.json.get('dimension') == 'two':
        data = getter_service.get_hierarchy1()

    return do_success_response(data)

