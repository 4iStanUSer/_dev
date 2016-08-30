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


def notfound_view(req):
    req.response.status = 404
    return render_to_response('templates/404.jinja2',
                              {'title': '404 Not Found'},
                              request=req)


def forbidden_view(req):
    next_url = req.route_url('common.login', _query={'next': req.url})
    return HTTPFound(location=next_url)


def index_view(req):
    #user = req.user
    #if user is None:
    #    raise HTTPForbidden

    # service.recreate_db(req)
    # service.fillin_db(req)


    return render_to_response('templates/index.jinja2',
                              {'title': 'Home page'},
                              request=req)


def login_view(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('common.index')
    message = ''
    email = ''
    # if 'form.submitted' in request.params:
    #     email = request.params['email']
    #     password = request.params['password']
    #     user = service.get_user_by_email(email)
    #     if user is not None: # and user.check_password(password)
    #         headers = remember(request, user.id)
    #         return HTTPFound(location=next_url, headers=headers)
    #     message = 'Failed login'

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
