from ..models.scenarios import Scenario
from ..models.access import User
from sqlalchemy.orm.exc import NoResultFound
import datetime


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
        scenario_info['description'] = scenario.description
        scenario_info['shared'] = scenario.shared
        scenario_info['author'] = scenario.author
        scenario_info['location'] = scenario.status
        scenario_info['modify_date'] = scenario.date_of_last_modification
        scenario_info_list.append(scenario_info)
    return scenario_info_list


def deserialise_scenario(scenario_info):
    """
    Serialise scenario into dictionary
    :param scenarios:
    :type scenarios:
    :return:
    :rtype:
    """
    scenario = Scenario(name = scenario_info['name'],
                        description = scenario_info['description'])
    #TODO entity selection
    #TODO predifinde driver

    return scenario


def create_scenario(request, input_data):

    try:
        date_of_last_mod = str(datetime.datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'], shared=input_data['shared'],
                        date_of_last_modification=date_of_last_mod, status="New", criteria=input_data['description'])
        request.dbsession.add(scenario)
    except NoResultFound:
        return None
    else:
        pass


#check permission
def copy_scenario(request, scenario_id):
    """
        Get scenario by specific filters

        :param request:
        :type request:
        :param filters - List of filters:
        :type filters: List
        :return:
        :rtype:
        """
    try:
        scenarios = request.dbsession.query(Scenario). \
            filter(Scenario.id == scenario_id).all()
        scenario_info_list = serialise_scenario(scenarios)
    except NoResultFound:
        return scenario_info_list
    else:
        return scenario_info_list


def get_scenarios(request, filters, author):
    """
    Get scenario by specific filters

    :param request:
    :type request:
    :param filters - List of filters:
    :type filters: List
    :return:
    :rtype:
    """
    try:
        user = request.dbsession.query(User).filter(User.id == author).one()
        if filters == {}:
            scenarios = user.scenarios
        else:
            scenarios = request.dbsession.query(Scenario). \
                filter(Scenario.name == filters['authors'] and Scenario.criteria.name == filters['criteria']).all()

        scenario_info_list = serialise_scenario(scenarios)
    except NoResultFound:
        return scenario_info_list
    else:
        return scenario_info_list


def update_scenario(request, scenario_id, parameter, value):
    """
    Update scenario by specific parameters

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        if parameter == "name":
            scenario.name = value
        elif parameter == "status":
            scenario.status = value
        else:
            pass
    except NoResultFound:
        return None
    else:
        return True


def check_scenario(request, scenario_id, new_values):
    """
    Check scenario on specific parameter value

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
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

    except NoResultFound:
        return None
    else:
        return True


def delete_scenario(request, scenario_id):
    """
    Delete scenario's
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        request.dbsession.delete(scenario)
    except NoResultFound:
        return None
    else:
        return True


def include_scenario(request):
    """
    Include scenarios
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass


def search_and_get_scenarios(request, scenario_id):
    """
    Search and get scenario's
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        user_id = 2#TODO change on request.get_user
    except NoResultFound:
        return None
    else:
        now = datetime.datetime.now()
        present_time = "{0}_{1}_{2}_{3}_{4}".format(now.year, now.month, now.day, now.hour, now.minute)
        scenario_details = {}

        scenario_details['id'] = scenario.id
        scenario_details['meta'] = scenario.criteria
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
