from iap.common.repository.models.scenarios import Scenario
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


def get_scenarios(request, filters):
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
        if all(filter == [] for filter in filters.values()):
            scenarios = request.dbsession.query(Scenario).all()
        else:
            scenarios = request.dbsession.query(Scenario). \
                filter(Scenario.name == filters['authors'] and Scenario.criteria.name == filters['criteria']).all()
        scenario_info_list = serialise_scenario(scenarios)
    except NoResultFound:
        return scenario_info_list
    else:
        return scenario_info_list


def update_scenario(request, scenario_id, new_values):
    """
    Update scenario by specific parameters

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
        serialized_scenario = serialise_scenario(scenario)
    except NoResultFound:
        return None
    else:
        return serialized_scenario


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
                assert scenario.name == new_values["name"]
                return True
            elif parameter == "status":
                assert scenario.name == new_values["status"]
                return True
            elif parameter == "shared":
                assert scenario.name == new_values["shared"]
                return True
            elif parameter == "description":
                assert scenario.name == new_values["description"]
                return True
            else:
                return False
    except NoResultFound:
        return None
    except AssertionError:
        return False
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
    try:
        parent_scenario = request.dbsession.query(Scenario).filter(Scenario.id == parent_scenario_id).one()
        current_scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        parent_scenario.children.append(current_scenario)
    except NoResultFound:
        msg = "No result"
        return msg
    else:
        msg  = "Scenario's included"
        return msg

def search_and_get_scenarios(request, parameter):
    """
    Search and get scenario's
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario = request.dbsession.query(Scenario).filter(Scenario.id == scenario_id).one()
        if parameter == "description":
            output = scenario.description
        else:
            output = "No requested item"
    except NoResultFound:
        return None
    else:
        return output

