from ...common.repository.models.scenarios import Scenario
from ...common.repository.models_managers import scenario_manager
from ...common.repository.models_managers import access_manager
from sqlalchemy.orm.exc import NoResultFound
import datetime


def serialise_scenario(scenarios, user):
    """Serialise scenario into dictionary
    :param scenarios:
    :type scenarios:
    :return:
    :rtype:
    """
    scenario_info_list = []

    scenario_permission = ['share', 'change_status', 'copy', 'delete', 'edit']
    for scenario in scenarios:
        scenario_info = {}
        scenario_info['id'] = scenario.id
        scenario_info['name'] = scenario.name
        scenario_info['status'] = scenario.status
        scenario_info['favorite'] = scenario.favorite
        scenario_info['description'] = scenario.description
        scenario_info['criteria'] = scenario.criteria
        scenario_info['shared'] = scenario.shared
        if user.email == scenario.author:
            scenario_info['scenario_permission'] = scenario_permission
        else:
            scenario_info['scenario_permission'] = ['copy']
        scenario_info['author'] = scenario.author
        scenario_info['modify_date'] = scenario.date_of_last_modification
        scenario_info_list.append(scenario_info)
    return scenario_info_list



def deserialise_scenario(scenario_info):
    """Serialise scenario into dictionary
    :param scenario_info:
    :type scenario_info:
    :return:
    :rtype:
    """
    scenario = Scenario(name=scenario_info['name'], description=scenario_info['description'])
    #TODO entity selection
    #TODO predifinde driver
    return scenario


def create_scenario(session, user_id, input_data):
    """Create scenario
    :param request:
    :type request:
    :param input_data:
    :type input_data:
    :return:
    :rtype:
    """
    try:
        #TODO check existense
        user = access_manager.get_user_by_id(session, user_id=user_id)
        input_data['author'] = user.email
        scenario = scenario_manager.create_scenario(session, input_data=input_data, user=user)
        serialised_scenario = serialise_scenario([scenario], user)
    except NoResultFound:
        raise NoResultFound
    else:
        return serialised_scenario


def get_scenario_page(session, user_id, filter=None):
    try:
        scenarios = scenario_manager.get_available_scenario(session, user_id, filter)
        user = access_manager.get_user_by_id(session, user_id)
    # TODO change field of tool_id in db.
        scenario_list = serialise_scenario(scenarios, user)
        user_permission = access_manager.get_feature_permission(session, user_id, 'forecast')#TODO change 1 on forecast)
    except NoResultFound:
        raise Exception
    else:
        result = {'data': scenario_list, 'user_permission': user_permission}
        return result


def copy_scenario(session, user_id, scenario_id):
    """Get scenario by specific filters
    :param session:
    :type session:
    :param user_id:
    :type user_id:
    :return:
    :rtype:
    """
    try:
        scenario = scenario_manager.get_scenario_by_id(session, user_id, scenario_id)
        user = access_manager.get_user_by_id(session, user_id)
        scenario_data = dict(name=scenario.name, description=scenario.description,
                             criteria=scenario.criteria, author=user.email, shared="No", status="Draft")
        scenario = scenario_manager.create_scenario(session, input_data=scenario_data, user=user)
        serialised_scenario = serialise_scenario([scenario], user)
        #TODO provide scenario coppying
    except NoResultFound:
        raise NoResultFound
    else:
        return serialised_scenario

def get_scenarios(session, user_id, filters):
    """
    Get scenario by specific filters

    :param session:
    :type session:
    :param user_id:
    :type user_id:
    :param filters - List of filters:
    :type filters: List
    :return:
    :rtype:
    """
    try:
        #TODO change on select all scenario
        user = access_manager.get_user_by_id(session, user_id)
        scenarios = scenario_manager.get_available_scenario(session, user_id, filters)
    except NoResultFound:
        raise Exception
    else:
        scenario_info_list = serialise_scenario(scenarios, user)
        return scenario_info_list


def check_scenario(session, scenario_id, user_id, new_values):
    """
    Check scenario on specific parameter value

    :param session:
    :type session:
    :param scenario_id:
    :type scenario_id:
    :param user_id:
    :type user_id:
    :param new_values:
    :type new_values:
    :return:
    :rtype:
    """
    try:
        scenario = scenario_manager.get_scenario_by_id(session, scenario_id, user_id)

        for parameter in new_values.keys():
            if parameter == "name":
                scenario.name = new_values["name"]
            elif parameter == "status":
                scenario.name = new_values["status"]
            elif parameter == "shared":
                scenario.name = new_values["shared"]
            elif parameter == "description":
                scenario.name = new_values["description"]

    except NoResultFound:
        return False
    else:
        return True


def search_and_get_scenarios(session, scenario_id, user_id):
    """
    Search and get scenario's
    :param session:
    :type session:
    :param scenario_id:
    :type scenario_id:
    :param user_id:
    :type user_id:
    :return:
    :rtype:
    """
    try:
        scenario = scenario_manager.get_scenario_by_id(session, scenario_id, user_id)
    except NoResultFound:
        return None
    else:
        now = datetime.datetime.now()
        present_time = "{0}_{1}_{2}_{3}_{4}".format(now.year, now.month, now.day, now.hour, now.minute)
        scenario_details = {}

        scenario_details['id'] = scenario.id
        scenario_details['meta'] = None
        scenario_details['criteria'] = scenario.criteria
        scenario_details['description'] = scenario.description
        scenario_details['worklist'] = [{'id': scenario.id, 'name': scenario.name, 'date': present_time}]
        scenario_details['metrics'] = [{"name": "", "format": "", "value": ""}]#TODO add metric
        scenario_details['growth_period'] = ""#TODO add growth period
        scenario_details['predefined_drivers'] = [{'id': "", 'value': ""}]
        scenario_details['predefined_drivers'] = [{'id': "", 'value': ""}]
        scenario_details['driver_change'] = [{'name': "", 'value': ""}]
        scenario_details['driver_group'] = [{'name': "", 'value': ""}]
        scenario_details['recent_actions'] = [{'action_id': "", 'action_name': "", 'entity_id': "",
                                          'entity_name': "", 'date': ""}]
        return scenario_details


def get_scenario_details(session, user_id, scenario_id):
    """Get scenario details

    :param session:
    :type session:
    :param user_id:
    :type user_id:
    :param scenario_id:
    :type scenario_id:
    :return:
    :rtype:
    """
    try:
        scenario = scenario_manager.get_scenario_by_id(session, user_id, scenario_id)
    except Exception:
        raise NoResultFound
    else:
        now = datetime.datetime.now()
        present_time = "{0}_{1}_{2}_{3}_{4}".format(now.year, now.month, now.day, now.hour, now.minute)
        scenario_details = {}
        scenario_details['id'] = scenario.id
        scenario_details['meta'] = None
        scenario_details['status'] = scenario.status
        scenario_details['name'] = scenario.name
        scenario_details['description'] = scenario.description
        scenario_details['worklist'] = [{'id': scenario.id, 'name': scenario.name, 'date': present_time}]
        scenario_details['metrics'] = [{"name": "", "format": "", "value": ""}]#TODO add metric
        scenario_details['growth_period'] = ""#TODO add growth period
        scenario_details['driver_change'] = [{'name': "", 'value': ""}]
        scenario_details['driver_group'] = [{'name': "", 'value': ""}]
        scenario_details['recent_actions'] = [{'action_id': "", 'action_name': "",
                                               'entity_id': "", 'entity_name': "", 'date': ""}]
        print()
    return scenario_details

#TODO add decorator
def update_scenario(session, scenario_id, user_id, parameter, value):
    """
    Update scenario by specific parameters

    :param session:
    :type session:
    :param scenario_id:
    :type scenario_id:
    :param user_id:
    :type user_id:
    :param parameter:
    :type parameter:
    :param value:
    :type value:
    :return:
    :rtype:
    """
    try:
        scenario = scenario_manager.get_scenario_by_id(session, scenario_id=scenario_id, user_id=user_id)

        user = access_manager.get_user_by_id(session, user_id)

        tool_id = 'forecast'
        #TODO add decorator
        if parameter == 'status' and value == 'final':
            feature_id = 'finalize'
        else:
            feature_id = 'edit'

        if access_manager.check_feature_permission(session, user_id, tool_id, feature_id) and \
                access_manager.check_scenario_permission(parameter=parameter, scenario=scenario, user=user):
            scenario_manager.update_scenario(scenario, parameter, value)
            status = True
        else:
            status = False

        value = scenario_manager.get_value(scenario, parameter)
    except Exception:
        return False, value
    else:

        return status, value
