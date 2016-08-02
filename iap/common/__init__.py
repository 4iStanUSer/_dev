#TODO move Login package here

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.response import Response
from pyramid.renderers import render_to_response

from . import tweens
from . import security
from . import service

def notfound_view(request):
    request.response.status = 404
    return {}

def forbidden_view(request):
    next_url = request.route_url('common.login', _query={'next': request.url})
    return HTTPFound(location=next_url)

def index_view(request):
    #user = request.user
    #if user is None:
    #    raise HTTPForbidden

    #return Response('<h1>Hello world!</h1>')
    return render_to_response('templates/index.jinja2',
                       {'title': 'Forecast index'},
                       request=request)

def login_view(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('common.index')
    message = ''
    email = ''
    if 'form.submitted' in request.params:
        email = request.params['email']
        password = request.params['password']
        user = service.get_user_by_email(email)
        if user is not None: # and user.check_password(password)
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    data = dict(
        message=message,
        url=request.route_url('common.login'),
        next_url=next_url,
        email=email,
        )
    return render_to_response('templates/login.jinja2',
                              data,
                              request=request)

def logout_view(request):
    headers = forget(request)
    next_url = request.route_url('common.login')
    return HTTPFound(location=next_url, headers=headers)