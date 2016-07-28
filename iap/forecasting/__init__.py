'''
Package - Forecasting tool(FT)
'''
#from pyramid.view import view_config
#from pyramid.response import Response
from pyramid.renderers import render_to_response

def index(request):
    return render_to_response('templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=request)
