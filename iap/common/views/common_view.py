from iap.common.repository.models.access import Tool, User, Feature, UserGroup, Role, Project
from pyramid.renderers import render_to_response
from pyramid.threadlocal import get_current_registry

from pyramid import threadlocal
from pyramid.paster import get_appsettings
from ...common.helper import send_success_response, send_error_response
from ...common.tools_config import get_page_config
from ...common.exceptions import *
from ...common import runtime_storage as rt
from ...common import persistent_storage as pt
from ..services import common_info as common_getter
from ..security import *


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
    try:
        user_id = get_user(req)
        session_flag = True#check_session(req)
    except JSONDecodeError:
        msg = req.get_error_msg("RequestError")
        return send_error_response(msg)
    except KeyError:
        msg = req.get_error_msg("RequestError")
        return send_error_response(msg)
    else:
        if user_id != None and session_flag == True:
            token = req.create_jwt_token(2, login="default_user")
            # new_token = req.session['token']
            return send_success_response(token)
    finally:
        #msg = req.get_error_msg('default', "NotFound")
        #return send_error_response("Unauthorised_{0}".format(msg))
        #TODO send_error_responce
        token = req.create_jwt_token(2, login="default_user")
        return send_success_response(token)


def login(req):
    """View function for login

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: Dict[str, str]

    """
    print("Registry", get_current_registry().settings)
    print(req)
    try:
        print("Registry", get_current_registry().settings)

        username = req.json_body['username']
        password = req.json_body['password']
    except KeyError:
        msg = req.get_error_msg("RequestError")
        return send_error_response(msg)
    except JSONDecodeError:
        msg = req.get_error_msg("RequestError")
        return send_error_response(msg)
    try:
        session = req.dbsession
        user_id, login = authorise(session, user_name=username, password=password)
    except NoResultFound as e:
        msg = req.get_error_msg("NoResultFound")
        return send_error_response("Unauthorised_{0}".format(msg))
    except AttributeError:
        msg = req.get_error_msg("NotFound")
        return send_error_response("Unauthorised_{0}".format(msg))
    except IncorrectPassword:
        msg = req.get_error_msg("IncorrectPassword")
        return send_error_response("Unauthorised_{0}".format(msg))
    else:
        token = req.create_jwt_token(user_id, login=login)
        req.session['token'] = token
        return send_success_response(token)


def logout(req):
    """
    Provide mechanism for session leaving
    """
    print(req)
    try:
        if 'token' in req.session:
            del req.session['token']
    except KeyError:
        msg = req.get_error_msg("NotFound")
        return send_error_response("Unauthorised_{0}".format(msg))
    else:
        return send_success_response("Session expired")


def get_routing_config(req):
    config = {
        '/get_landing': {'url': '/get_landing', 'allowNotAuth': True}
    }
    return send_success_response(config)

@forbidden_view
def get_page_configuration(req):
    """

    View for url - get_page_configuration
    By given (String) user_id and page_name
    Return (Dictionary) with Widgets Names

    Example:
    View Page Configuration
        {'top_menu***simulator': 'Simulator',
        'top_menu***scenarios': 'Scenarios',
        'top_menu***landing': 'Home',
        'top_menu***help': 'Help',
        'logout***label': 'Log Out',
        'top_menu***comparison': 'Comparison',
        'top_menu***dashboard': 'Dashboard'}


    :param req:
    :type req:
    :return:
    :rtype:
    """
    # Get parameters from request.
    try:
        user_id = req.user
        page_name = req.json_body['data']['page']
    except KeyError as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    try:
        state = rt.get_state(user_id)
        tool_id = state.tool_id
        language = state.language
        config = get_page_config(tool_id, page_name, language)
        return send_success_response(config)
    except Exception as e:
        msg = req.get_error_msg(e, language)
        return send_error_response(msg)

@forbidden_view
def set_language(req):
    """
    View for set language in runtime storage
    Call update state with new language
    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = req.user
        lang = req.json_body['data']['lang']
    except KeyError as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    try:
        rt.update_state(user_id, language=lang)
        return send_success_response()
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


@forbidden_view
def get_tools_with_projects(req):
    """
    Return all projects and tool information
    TODO remake to query from database

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: None
    """
    try:
        user_id = req.user
    except KeyError as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    try:
        data = dict()
        if not user_id:
            data['tools'] = common_getter.get_tools_info(pt)
        else:
        #TODO call acccess manager  - check permission to project_id, tool_id
            lang = rt.get_state(user_id).language
            data['tools'] = common_getter.get_tools_info(req, lang)
            data['projects'] = common_getter.get_projects_info(req, lang)
        return send_success_response(data)
    except Exception as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)


@forbidden_view
def get_data_for_header(req):
    """
    View for url - get_data_for_header(request)
    Args:
        user_id
    Return:
        (Dict) {'user':{}, 'language':{}, 'client':{}}
    Example:
        Header Data
        {'client': {'icon': 'logo.jpg', 'name': 'CompanyASD'},
         'user': {'name': 'Nicolas'},
         'languages': [{'id': 'en', 'selected': True, 'name': 'English'},
                      {'id': 'ru', 'selected': False, 'name': 'Russian'}]
         }

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = req.user
    except KeyError as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    try:
        header_data = dict()
        lang = rt.get_state(user_id).language
        #TODO change on database access
        header_data['languages'] = common_getter.get_languages_list(pt, lang)
        header_data['user'] = common_getter.get_user_info(pt, user_id, lang)
        header_data['client'] = common_getter.get_client_info(pt, user_id, lang)
        return send_success_response(header_data)
    except Exception as e:
        msg = req.get_error_msg(e, lang=lang)
        return send_error_response(msg)

#@forbidden_view
def set_project_selection(req):
    """Set project selector

    Args:
        project_id:(String)
        tool_id:(String)
    Return:
        project_id with updated status in runtime storage

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = req.user
        project_id = req.json_body['data']['project_id']
        tool_name = req.json_body['data']['tool_id']
    except KeyError as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    try:
        #TODO Change accesss for project selector
        #TODO Check That project existed
        lang = rt.get_state(user_id).language
        rt.update_state(user_id, tool_id=tool_name, project_id=project_id)
        return send_success_response(project_id)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


def process_data(req):
    """
    View for data processing

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        config_name = req.json_body['config_name']
    except KeyError:
        from iap.data_loading.data_loader import Loader
        import logging
        settings = ""
        loader = Loader()
        loader.run_processing(config_name)
        return  send_success_response()