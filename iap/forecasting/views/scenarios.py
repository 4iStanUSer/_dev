from ...repository.db.models_access import Scenario, User
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
import datetime

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
        print(input_data)
        print(request.dbsession.query(Scenario).all())
        #check user permisssion
        #_criteria = request.dbsession.query(Entity).filter(Entity._dimension_name == input_data['geographies'] and
        #                            Entity._layer==input_data['channel'] and Entity._name==input_data['product'])
        date_of_last_mod = str(datetime.datetime.now())
        print('+')
        scenario = Scenario(name=input_data['name'], description=input_data['description'],date_of_last_modification=date_of_last_mod, status="New")
        print(scenario)
        request.dbsession.add(scenario)
        request.commit()
    except:
        return send_error_response("Failed to create scenario")
    else:
        return send_success_response("Scenario created")


def search_and_view_scenario(request, *kwarg):

    scenario = request.dbsession.query(Scenario).filter()
    pass

def get_scenario_description(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['id']
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        description = scenario.description
    except:
        return send_error_response("Failed to get scenario description")
    else:
        return send_success_response(description)

def change_scenario_name(request):
    """
    Change scenario name

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['scenario_id']
        new_name = request.json_body['new_name']
        scenario = request.dbconn.query(Scenario).filter(Scenario.id == scenario_id).one()
        scenario.update({Scenario.name:new_name})
        request.dbconn.commit()
    except:
        return send_error_response("Failed to change name")
    else:
        return send_success_response("Name changed")


def check_scenario_name(request):
    pass


def modify(request):
    """

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        new_values = request.json_body['modification']
        scenario_id = request.json_body['scenario_id']
        for parameter in new_values.keys():
            request.dbconn.query(Scenario).filter(Scenario.id == scenario_id).update({parameter: new_values[parameter]})
    except:
        return send_error_response("Failed to modify selcted scenario")
    else:
        return send_success_response(new_values)


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
        scenario_id = request.json_body['scenario_id']
        request.dbconn.query(Scenario).filter(Scenario.id == scenario_id).delete()
        request.dbconn.commit()
        return send_success_response("Deleted selected scenario")
    except:
        return send_error_response("Failed to delet selcted scenario")

def publish(request):
    """Publish selected scenario to central repository
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass

def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['scenario_id']
        request.dbconn.query(Scenario).filter(Scenario.id==scenario_id).update({'status':'final'})
        request.dbconn.commit()
        return send_success_response("Marked as final")
    except:
        return send_error_response("Marking as final failed")


def incude_scenario(request):
    try:
        parent_scenario_id = request.json_body['parent_scenario_id']
        scenario_id = request.json_body['scenario_id']
        parent_scenario = request.dbconn.query(Scenario).filter(Scenario.id == parent_scenario_id).one()
        current_scenario = request.dbconn.query(Scenario).filter(Scenario.id == scenario_id).one()
        parent_scenario.update({'children': current_scenario})
        request.dbconn.commit()
        return send_success_response("Include finished successive")
    except:
        return send_error_response("Failed to include")

#@forbidden_view
#@requires_roles()
def get_scenarios_list(req):
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
