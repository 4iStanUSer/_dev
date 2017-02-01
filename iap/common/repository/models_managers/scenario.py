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
        scenario_info['shared'] = scenario.shared
        scenario_info_list.append(scenario_info)
    return scenario_info_list


def create_scenario(request, input_data):

    try:
        date_of_last_mod = str(datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'], shared=input_data['shared'],
                        date_of_last_modification=date_of_last_mod, status="New", criteria=input_data['description'])
        request.dbsession.add(scenario)
    except NoResultFound:
        return None
    else:
        pass


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


def update_scenatio(request,scenario_id, parameter, value):
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


def search_and_get_scenarios(request):
    """
    Search and get scenario's
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass


def include_scenarions(request):
    pass
