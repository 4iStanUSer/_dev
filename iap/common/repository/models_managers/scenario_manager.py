from ..models.scenarios import Scenario
from ..models.access import User
from sqlalchemy.orm.exc import NoResultFound
from ..models_managers import access_manager
import transaction
import datetime


def create_scenario(session, input_data, user=None):
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
        date_of_last_mod = str(datetime.datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'],
                            shared=input_data.get('shared', None), date_of_last_modification=date_of_last_mod,
                            status=input_data.get('status', None),
                            criteria=input_data['criteria'],
                            author=input_data['author'],
                            )
        session.add(scenario)
        if user:
            user.scenarios.append(scenario)

    except NoResultFound:
        raise NoResultFound
    else:
        return scenario


def get_scenario_by_id(session, user_id, scenario_id):

    query = session.query(Scenario)
    query = query.join(User.scenarios)
    query = query.filter(Scenario.id == scenario_id)
    query = query.filter(User.id == user_id)
    scenario = query.one()
    return scenario


def get_available_scenario(session, user_id, filters=None):
    """
    Return all available scenarios

    :param session:
    :type session:
    :param filters:
    :type filters:
    :param author:
    :type author:
    :return:
    :rtype:
    """
    try:
        scenarios = session.query(Scenario)
        scenarios = scenarios.join(Scenario.users)
        scenarios = scenarios.filter(User.id == user_id).all()
    except NoResultFound:
        raise Exception
    try:
        if filters:
            pass
        else:
            pass
    except Exception:
        raise Exception
    else:
        return scenarios


def get_own_scenarios(session, user_id, filters):
    """
    Get scenario by specific filters

    :param request:
    :type request:
    :param filters - List of filters:
    :type filters: List
    :param author:
    :type author:
    :return:
    :rtype:
    """
    try:
        scenarios = session.query(Scenario)
        scenarios = scenarios.join(Scenario.users)
        scenarios = scenarios.filter(User.id == user_id)
        scenarios = scenarios.filter(Scenario.author == user_id)
    except NoResultFound:
        raise Exception
    else:
        return scenarios


def include_scenario(session, user_id, scenario_id, parent_scenario_id):

    scenario = get_scenario_by_id(session, user_id, scenario_id)
    parent_scenario = get_scenario_by_id(session, user_id, parent_scenario_id)
    parent_scenario.children.append(scenario)
    return


def update_scenario(scenario, parameter, value):

    if getattr(scenario, parameter) == str(value):
        pass
    else:
        setattr(scenario, parameter, str(value))
    return


def get_value(scenario, parameter):
    return getattr(scenario, parameter)


def delete_scenario(session, scenario_id, user_id):
    """
    Delete scenario's
    :param session:
    :type session:
    :param scenario_id:
    :type integer:
    :param user_id:
    :type integer:
    :return:
    :rtype:
    """
    try:
        user = access_manager.get_user_by_id(session, user_id=user_id)
        scenario = get_scenario_by_id(session, scenario_id=scenario_id, user_id=user_id)
        if scenario.author == user.email:
            session.delete(scenario)
            status = "Deleted"
        else:
            status = "Unauthorised"
    except NoResultFound:
        return "No item"
    else:
        return status