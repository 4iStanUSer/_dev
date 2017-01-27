from ...repository.db.models_access import Tool, User, Feature, UserGroup, Role
from ...repository.db.models import Project,Pr_Tool
from pyramid.renderers import render_to_response
from pyramid import threadlocal
from pyramid.paster import get_appsettings
from ...common.helper import send_success_response, send_error_response
from ...common.tools_config import get_page_config
from ...common.error_manager import ErrorManager
from ...common import exceptions as ex
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
    user_id = get_user(req)
    session_flag = check_session(req)

    if user_id != None and session_flag == True:
        new_token = req.session['token']
        return send_success_response(new_token)
    else:
        return send_error_response('Unauthorised')


def login(req):
    """View function for

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: Dict[str, str]

    """
    user = authorise(req)
    if user != None:
        user_id = user.id
        login = user.email
        token = req.create_jwt_token(user_id, login=login)
        req.session['token'] = token
        return send_success_response(token)
    else:
        return send_error_response("Unauthorised")



def logout(req):
    """
    Provide mechanism for session leaving
    """
    if 'token' in req.session:
        del req.session['token']
    return send_success_response("Session expired")


def get_routing_config(req):
    config = {
        '/get_landing': {'url': '/get_landing', 'allowNotAuth': True}
    }
    return send_success_response(config)


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
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        state = rt.get_state(user_id)
        tool_id = state.tool_id
        language = state.language
        #get page confiduration by tool_id, page_name, language
        config = get_page_config(tool_id, page_name, language)
        return send_success_response(config)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def set_language(req):
    """
    View for set language in runtime storage
    Call update state with new language
    :param req:
    :type req:
    :return:
    :rtype:
    """
    # Get parameters from request.
    try:
        user_id = req.user
        lang = req.json_body['data']['lang']
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
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        data = dict()
        if not user_id:
            data['tools'] = common_getter.get_tools_info(pt)
        else:
            #call acccess manager  - check permission to project_id, tool_id
            #lang = rt.get_state(user_id).language
            #tools_ids, projects_ids = pt.get_user_tools_with_projects(user_id)
            #data['tools'] = common_getter.get_tools_info(req, pt, tools_ids, lang)
            data['tools'] = common_getter.get_tools_info(req)
            #data['projects'] = common_getter.get_projects_info(req, pt, projects_ids, lang)
            data['projects'] = common_getter.get_projects_info(req)
        return send_success_response(data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


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
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        header_data = dict()
        lang = rt.get_state(user_id).language
        header_data['languages'] = common_getter.get_languages_list(pt, lang)
        header_data['user'] = common_getter.get_user_info(pt, user_id, lang)
        header_data['client'] = common_getter.get_client_info(pt, user_id, lang)
        return send_success_response(header_data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def set_project_selection(req):

    try:
        user_id = req.user
        project_id = req.json_body['data']['project_id']
        tool_name = req.json_body['data']['tool_id']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        #Change accesss for project selector
        project = req.dbsession.query(Project).filter(Project.id == project_id).one()
        #update state of runtime storage
        rt.update_state(user_id, tool_id=tool_name, project_id=project.id)
        return send_success_response(project_id)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)



def test_preparation(request):
    """
    Function called before each gunctional test executed
    Create table if it needed fill database with neccessary data
    :param request:
    :type request:
    :return:
    :rtype:
    """

    from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
    test_name = request.json_body['test_name']
    if test_name == "scenario":
        create_table(request)
        prepare_scenario_testing(request)
        return send_success_response("Test Prepared")
    elif test_name == "authentification":
        prepare_scenario_testing(request)
        return send_success_response("Test Prepared")
    if test_name == "authorisation":
        prepare_scenario_testing(request)

    if test_name == "project_creation":
        from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
        prepare_scenario_testing(request)
    pass

