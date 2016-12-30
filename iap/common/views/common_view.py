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
    #add session verification
    if get_user(req) == Exception: #check_session(req) == False:
        return send_error_response('Unauthorised')
    elif get_user(req)!= Exception and check_session(req) == True:
        new_token = req.session['token']
        return send_success_response(new_token)


def login(req):
    """View function for

    :param req:
    :type req: pyramid.util.Request
    :return:
    :rtype: Dict[str, str]

    """
    user = authorise(req)
    print(user)
    if user == Exception:
        return send_error_response('Unauthorised')
    else:
        user_id = user.id
        login = user.email
        print('User', user_id)
        token = req.create_jwt_token(user_id, login=login)
        req.session['token'] = token
        return send_success_response(token)


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
    View for get_page_configuration
    By givem user_id and page_name
    :param req:
    :type req:
    :return:
    :rtype:
    """
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
        user_id = get_user(req).id
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        data = dict()
        if not user_id:
            data['tools'] = common_getter.get_tools_info(pt)
        else:
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
    try:
        user_id = req.user.id
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



def test_preparation(request):
    """
    Function called before each gunctional test executed
    Create table if it needed fill database with neccessary data
    :param request:
    :type request:
    :return:
    :rtype:
    """
    test_name = request.json_body['test_name']
    if test_name == "scenario":
            #1.1 create table
            from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
            create_table(request)
            prepare_scenario_testing(request)
            #1.2 add entity
            #from iap.repository.db.warehouse import Entity
            #entity = Entity(_name="Nike", _dimension_name="Brazil",_layer="Main")
            #request.dbsession.add(entity)
            #1.3 create user and set role
            from iap.repository.db.models_access import User
            new_user = User(email="default_user", password="123456")
            request.dbsession.add(new_user)
            return send_success_response("Test Prepared")
    elif test_name == "authentification":
        from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
        from iap.repository.db.models_access import User, Role, UserGroup, DataPermissionAccess
        prepare_scenario_testing(request)
        #1.1 create User
        new_user = User(email="default_user", password="123456")
        request.dbsession.add(new_user)
        #1.2 add entity add role,group

        #1.3 set permission for user
        return send_success_response("Test Prepared")
    if test_name == "authorisation":
        from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
        from iap.repository.db.models_access import User, Role, UserGroup, DataPermissionAccess
        prepare_scenario_testing(request)
        #1.1 create User
        new_user = User(email="default_user", password="123456")
        request.dbsession.add(new_user)
        #1.2 set Role
        role = Role(name="forecaster")
        request.dbsession.add(role)
        new_user.roles.append(role)
        role.users.append(new_user)
    if test_name == "project_creation":
        from ...forecasting.views.scenarios import create_table, prepare_scenario_testing
        prepare_scenario_testing(request)
        #1.1 create Project
        #1.2 create fill db
    pass



def model_overview(req):
    """
    To Do refactor

    :param req:
    :type req:
    :return:
    :rtype:

    """
    req.dbsession.query(Tool).delete()
    req.dbsession.query(Role).delete()
    req.dbsession.query(Feature).delete()
    data = req.json_body['data']
    for tool_name in data['Tool'].keys():
        tool = Tool(name = tool_name)
        if data['Tool'][tool_name]=={}:
            pass
        else:
            for feature_name in data['Tool'][tool_name]['Features'].keys():
                feature = Feature(name=feature_name)
                tool.features.append(feature)
                for role_name in data['Tool'][tool_name]['Features'][feature_name]['Roles']:
                    role = Role(name = role_name)
                    feature.roles.append(role)
                    tool.roles.append(role)
                    req.dbsession.add(role)
                req.dbsession.add(feature)
            req.dbsession.add(tool)
    users = []
    features = []
    tools = []
    roles = []
    for user in req.dbsession.query(User).all():
        users.append(user.id)
        users.append(user.email)
    for tool in req.dbsession.query(Tool).all():
        tools.append(tool.name)
    for role in req.dbsession.query(Role).all():
        roles.append(role.name)
    for feature in req.dbsession.query(Feature).all():
        features.append(feature.name)
    urls = [req.current_route_url(), req.current_route_path()]
    return {'users': users, 'tools': tools, 'roles': roles, 'features':features, "urls": urls}


def create_table(request):
    from iap.repository.db.meta import Base
    _engine = request.dbsession.bind.engine
    # Create all tables
    Base.metadata.create_all(_engine)
    tool = Pr_Tool(name='Forecasting', description='This is forecasting')
    request.dbsession.add(tool)

    project_1 = Project(name='Oral Care Forecasting')
    project_1.pr_tools.append(tool)
    request.dbsession.add(project_1)

    project_2 = Project(name='Lean Forecasting')
    project_2.pr_tools.append(tool)
    request.dbsession.add(project_2)