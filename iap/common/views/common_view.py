from pyramid.renderers import render_to_response
from ...common.helper import send_success_response, send_error_response
from ...common.tools_config import get_page_config
from ...common.error_manager import ErrorManager
from ...common import exceptions as ex
from ...common import runtime_storage as rt
from ...common import persistent_storage as pt
from ..services import common_info as common_getter
from ...common.security import authorise
from ...common.security import *
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import authenticated_userid
from pyramid.security import unauthenticated_userid
from pyramid.security import Authenticated
from iap.repository.db.models_access import User
import jwt

def index_view(req):
    return render_to_response('iap.common:templates/index.jinja2',
                              {'title': 'Home page'},
                              request=req)


def check_logged_in(req):
    """Check user existed

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: Dict[str, bool]

    """
    #add session verification
    if get_user(req) == Exception or check_session(req) == False:
        return send_error_response('Unauthorised')
    elif get_user(req)!=Exception and check_session(req) == True:
        new_token = req.session['token']
        return send_success_response(new_token)


def forbidden_view(f):
    def deco(request):
        user_id = get_user(request)
        if user_id != Exception and check_session(request) == True:
            return f(request)
        else:
            return send_error_response('Unauthorised')
    return deco


def login(req):
    """View function for

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: Dict[str, str]

    """
    user = authorise(req)
    if user==Exception:
        return send_error_response('Unauthorised')
    else:
        user_id = user.id
        login = user.email
        print('User', user_id)
        token = req.create_jwt_token(user_id, login=login)
        req.session['token'] = token
        return send_success_response(token)


def logout(req):
    #provide mechanism for session leaving
    del req.session['token']
    return send_success_response("")


def get_routing_config(req):
    config = {
        '/get_landing': {'url': '/get_landing', 'allowNotAuth': True}
    }
    return send_success_response(config)



def get_page_configuration(req):
    # Get parameters from request.
    try:
        user_id = req.user
        page_name = req.json_body['page']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        state = rt.get_state(user_id)
        tool_id = state.tool_id
        language = state.language
        config = get_page_config(tool_id, page_name, language)
        return send_success_response(config)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def set_language(req):
    # Get parameters from request.
    try:
        user_id = req.user
        lang = req.json_body['lang']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        rt.update_state(user_id, language=lang)
        return send_success_response()
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_tools_with_projects(req):
    try:
        user_id = req.user
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        data = dict()
        if not user_id:
            data['tools'] = common_getter.get_tools_info(pt)
        else:
            lang = rt.get_state(user_id).language
            tools_ids, projects_ids = pt.get_user_tools_with_projects(user_id)
            data['tools'] = common_getter.get_tools_info(pt, tools_ids, lang)
            data['projects'] = common_getter.get_projects_info(pt, projects_ids, lang)
        return send_success_response(data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_data_for_header(req):
    try:
        user_id = req.user
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        header_data = dict()
        lang = rt.get_state(user_id).language
        header_data['languages'] = common_getter.get_languages_list(pt, lang)
        header_data['user'] = common_getter.get_user_info(pt, user_id, lang)
        header_data['client'] = common_getter.get_client_info(pt, user_id,
                                                              lang)
        return send_success_response(header_data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def set_project_selection(req):
    try:
        user_id = req.user
        project_id = req.json_body['project_id']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        project = pt.get_project(id=project_id)
        rt.update_state(user_id, tool_id=project.tool_id, project_id=project.id)
        return send_success_response()
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)