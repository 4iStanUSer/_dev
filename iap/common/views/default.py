from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.renderers import render_to_response

from ...common.helper import send_success_response, send_error_response
from ...common.tools_config import get_page_config
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import rt_storage


def notfound_view(req):
    req.response.status = 404
    return render_to_response('iap.common:templates/404.jinja2',
                              {'title': '404 Not Found'},
                              request=req)


def forbidden_view(req):
    next_url = req.route_url('common.login', _query={'next': req.url})
    return HTTPFound(location=next_url)


def login_view(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('common.index')
    message = ''
    email = ''
    data = dict(
        message=message,
        url=request.route_url('common.login'),
        next_url=next_url,
        email=email,
    )
    return render_to_response('iap.common:templates/login.jinja2',
                              data,
                              request=request)


def logout_view(request):
    headers = forget(request)
    next_url = request.route_url('common.login')
    return HTTPFound(location=next_url, headers=headers)


def index_view(req):
    return render_to_response('iap.common:templates/index.jinja2',
                              {'title': 'Home page'},
                              request=req)


def get_page_configuration(req):
    # Get parameters from request.
    try:
        user_id = req.user
        page_name = 'dashboard'
        state = rt_storage.get_state(user_id)
        tool_id = state['tool_id']
        language = state['language']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)

    try:
        config = get_page_config(tool_id, page_name, language)
        return send_error_response(config)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)