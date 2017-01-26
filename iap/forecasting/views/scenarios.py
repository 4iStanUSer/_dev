from ...common.repository.db.models_access import Scenario, User, Feature, Role,Permission
from ...common.repository.db.warehouse import Entity
from sqlalchemy.orm.exc import NoResultFound
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
import datetime


def create_table(request):
    """
    Create Scenario Table
    :param request:
    :type request:
    :return:
    :rtype:
    """
    from iap.common.repository.db.meta import Base
    _engine = request.dbsession.bind.engine
    # Create all tables
    Base.metadata.create_all(_engine)


def prepare_scenario_testing(request):
    """
    Prepare db for testing
    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: None
    """
    scenarios = request.dbsession.query(Scenario).all()
    for scenario in scenarios:
        request.dbsession.delete(scenario)


def serialise_scenario(scenarios):
    """
    Serialise scenario into dictionary
    :param scenarios:
    :type scenarios:
    :return:
    :rtype:
    """
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
@requires_roles('Create a new scenario')
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
        input_data = request.json_body['data']
        date_of_last_mod = str(datetime.datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'],shared=input_data['shared'],
                        date_of_last_modification=date_of_last_mod, status="New", criteria=input_data['description'])
        request.dbsession.add(scenario)
    except NoResultFound:
        return send_error_response("Failed to create scenario")
    except KeyError:
        return send_error_response("Failed to create scenario")
    else:
        return send_success_response("Scenario created")


@forbidden_view
@requires_roles('View Scenario')
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
    try:
        filters = request.json_body['data']['filters']
        if all(filter == [] for filter in filters.values()):
            scenarios = request.dbsession.query(Scenario).all()
        else:
            scenarios = request.dbsession.query(Scenario).\
                filter(Scenario.name == filters['authors'] and Scenario.criteria.name == filters['criteria']).all()

        scenario_info_list = serialise_scenario(scenarios)
    except:
        return send_error_response("Error during searching")
    else:
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles('View Scenario')
def get_scenario_description(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id==scenario_id).one()
        description = scenario.description
    except KeyError:
        return send_error_response("Failed to get scenario description")
    except NoResultFound:
        return send_error_response("Failed to get scenario description")
    else:
        return send_success_response(description)


@forbidden_view
@requires_roles('View Scenario')
def change_scenario_name(request):
    """
    Change scenario name

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        new_name = request.json_body['data']['new_name']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        scenario.name = new_name
    except KeyError:
        return send_error_response("Failed to change name")
    except NoResultFound:
        return send_error_response("Failed to change name")
    else:
        return send_success_response("Name changed")


@forbidden_view
@requires_roles('View Scenario')
def check_scenario_name(request):
    try:
        scenario_id = request.json_body['data']['id']
        name = request.json_body['data']['name']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
    except KeyError:
        return send_error_response("Failed to change name")
    except NoResultFound:
        return send_error_response("Failed to change name")
    else:
        if scenario.name == name:
            return send_success_response("Name changed")
        else:
            return send_error_response("Failed to change name")


@forbidden_view
@requires_roles('Modify Scenario')
def modify(request):
    """
    Modify scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        new_values = request.json_body['data']['modification_value']
        scenario_id = request.json_body['data']['scenario_id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        for parameter in new_values.keys():
            if parameter == "name":
                scenario.name = new_values['data']["name"]
            elif parameter == "status":
                scenario.name = new_values['data']["status"]
            elif parameter == "shared":
                scenario.name = new_values['data']["shared"]
            elif parameter == "description":
                scenario.name = new_values['data']["description"]
    except KeyError:
        return send_error_response("Failed to modify selected scenario")
    except NoResultFound:
        return send_error_response("Failed to modify selected scenario")
    else:
        scenario_info_list = serialise_scenario(list(scenario))
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles('Delete Scenario')
def delete(request):
    """
    Delete selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        request.dbsession.delete(scenario)
    except KeyError:
        return send_error_response("Failed to delete selected scenario")
    except NoResultFound:
        return send_error_response("Failed to delete selected scenario")
    else:
        return send_success_response("Deleted selected scenario")


@forbidden_view
@requires_roles('Publish Scenario')
def publish_scenario(request):
    """Publish selected scenario to central repository
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass


@forbidden_view
@requires_roles('View Scenario')
def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    #ToDo - check is scenario already marked

    try:
        scenario_id = request.json_body['data']['id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        scenario.status = "final"
    except KeyError:
        return send_error_response("Marking as final failed")
    except NoResultFound:
        return send_error_response("Marking as final failed")
    else:
        return send_success_response("Mark as final")


@forbidden_view
@requires_roles('Include_scenario')
def include_scenario(request):

    try:
        parent_scenario_id = request.json_body['data']['parent_scenario_id']
        scenario_id = request.json_body['data']['scenario_id']
        parent_scenario = request.dbsession.query(Scenario).filter(Scenario.id == parent_scenario_id).one()
        current_scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        parent_scenario.children.append(current_scenario)
        return send_success_response("Include finished successive")
    except KeyError:
        return send_error_response("Failed to include")
    except NoResultFound:
        return send_error_response("Failed to include")


@forbidden_view
@requires_roles('View Scenario')
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
