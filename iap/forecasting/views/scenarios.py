from ...repository.db.models_access import Scenario, User
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
import datetime


def create_table(request):
    from iap.repository.db.meta import Base
    _engine = request.dbsession.bind.engine
    # Create all tables
    Base.metadata.create_all(_engine)

def prepare_scenario_testing(request):
    scenarios = request.dbsession.query(Scenario).all()
    for scenario in scenarios:
        print(scenario.id)
        request.dbsession.delete(scenario)

def serialise_scenario(scenarios):
    scenario_info_list = []
    scenario_info = {}
    for scenario in scenarios:
        scenario_info['id'] = scenario.id
        scenario_info['name'] = scenario.name
        scenario_info['status'] = scenario.status
        scenario_info['shared'] = scenario.shared
        scenario_info_list.append(scenario_info)
    return scenario_info_list


@forbidden_view
@requires_roles()
def create_scenario(request):
    """Function for creating new scenario
    args:
        scenario name
        scenario description
        geographies that scenario encompass
        product that scenario encompass
        chanell that scenario encompass
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        input_data = request.json_body
        #_criteria = request.dbsession.query(Entity).filter(Entity._dimension_name == input_data['geographies'] and
        #                            Entity._layer==input_data['channel'] and Entity._name==input_data['product'])
        date_of_last_mod = str(datetime.datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'],shared = input_data['shared'],
                            date_of_last_modification=date_of_last_mod, status="New")
        #scenario.criteria = criteria
        #scenario.authoe = user
        request.dbsession.add(scenario)

    except:
        return send_error_response("Failed to create scenario")
    else:
        return send_success_response("Scenario created")


@forbidden_view
@requires_roles()
def search_and_view_scenario(request):
    """
    Return list of scenario by given filters

    :param request:
    :type request:
    :param kwarg:
    :type kwarg:
    :return:
    :rtype:
    """
    scenario_info_list = []
    scenario_info = {}
    try:
        filters = request.json_body['filters']
        if all(filter == [] for filter in filters.values()):
            scenarios = request.dbsession.query(Scenario).all()
        else:
            scenarios = request.dbsession.query(Scenario).\
                filter(Scenario.name == filters['authors'] and Scenario.criteria.name == filters['criteria']).all()

        for scenario in scenarios:
            scenario_info['id'] = scenario.id
            scenario_info['name'] = scenario.name
            scenario_info['status'] = scenario.status
            scenario_info['shared'] = scenario.shared
            scenario_info_list.append(scenario_info)
    except:
        return send_error_response("Error during searching")
    else:
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles()
def get_scenario_description(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """
    scenario_info = {}
    try:
        scenario_id = request.json_body['id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id==scenario_id).one()
        description = scenario.description
    except:
        return send_error_response("Failed to get scenario description")
    else:
        return send_success_response(description)

@forbidden_view
@requires_roles()
def change_scenario_name(request):
    """
    Change scenario name

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['id']
        new_name = request.json_body['new_name']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        scenario.name = new_name
    except:
        return send_error_response("Failed to change name")
    else:
        return send_success_response("Name changed")


@forbidden_view
@requires_roles()
def check_scenario_name(request):
    try:
        scenario_id = request.json_body['id']
        name = request.json_body['name']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        if scenario.name == name:
            return send_success_response("Name changed")
    except:
        return send_error_response("Failed to change name")
    else:
        return send_error_response("Failed to change name")


@forbidden_view
@requires_roles()
def modify(request):
    """
    Modify scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        new_values = request.json_body['modification_value']
        scenario_id = request.json_body['scenario_id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        for parameter in new_values.keys():
            if parameter == "name":
                scenario.name = new_values["name"]
            elif parameter == "status":
                scenario.name = new_values["status"]
            elif parameter == "shared":
                scenario.name = new_values["shared"]
            elif parameter == "description":
                scenario.name = new_values["description"]
    except:
        return send_error_response("Failed to modify selected scenario")
    else:
        scenario_info_list = serialise_scenario(list(scenario))
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles()
def delete(request):
    """
    Delete selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    #firstly check access right for current function
    try:
        scenario_id = request.json_body['id']
        print(scenario_id)
        print([i.id for i in request.dbsession.query(Scenario).all()])
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        request.dbsession.delete(scenario)
    except:
        return send_error_response("Failed to delete selected scenario")
    else:
        return send_success_response("Deleted selected scenario")


@forbidden_view
@requires_roles()
def publish_scenario(request):
    """Publish selected scenario to central repository
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass


@forbidden_view
@requires_roles()
def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['id']
        print(scenario_id)
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        print('scenario', scenario)
        scenario.status = "final"
    except:
        return send_error_response("Marking as final failed")
    else:
        return send_success_response("Mark as final")


@forbidden_view
@requires_roles()
def include_scenario(request):

    try:
        parent_scenario_id = request.json_body['parent_scenario_id']
        scenario_id = request.json_body['scenario_id']
        parent_scenario = request.dbsession.query(Scenario).filter(Scenario.id == parent_scenario_id).one()
        current_scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        parent_scenario.children.append(current_scenario)
        return send_success_response("Include finished successive")
    except:
        return send_error_response("Failed to include")


@forbidden_view
@requires_roles()
def get_scenarios_list(request):
    scenarios = [
        {
            'id': 1,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 2,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': True,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 3,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 4,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        },
        {
            'id': 5,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 6,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 7,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 8,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        }
    ]

    return send_success_response(scenarios)
