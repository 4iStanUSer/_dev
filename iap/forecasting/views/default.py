from pyramid.renderers import render_to_response
from ..services import getter as getter_service


def index(request):
    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=request)


def get_time_series(request):
    return getter_service.get_time_series()
