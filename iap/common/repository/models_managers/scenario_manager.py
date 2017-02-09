from ..models.scenarios import Scenario
from ..models.access import User
from sqlalchemy.orm.exc import NoResultFound
import datetime


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
        date_of_last_mod = str(datetime.datetime.now())
        scenario = Scenario(name=input_data['name'], description=input_data['description'],
                            shared=input_data['shared'], date_of_last_modification=date_of_last_mod,
                            status="New", criteria=input_data['criteria'], author=user_id)
        session.add(scenario)

        user = session.query(User).filter(User.id == user_id).one()
        user.scenarios.append(scenario)
    except NoResultFound:
        raise NoResultFound


def get_scenario_by_id(session,user_id, scenario_id):

    query = session.query(Scenario)
    query = query.join(User.scenarios)
    query = query.filter(Scenario.id == scenario_id)
    query = query.filter(User.id == user_id)
    scenario = query.one()
    #scenario = query.filter(User.id == user_id).one()
    #else:
        # TODO join with user_id
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
        scenario = get_scenario_by_id(session, scenario_id, user_id)
        session.dbsession.delete(scenario)
    except NoResultFound:
        raise NoResultFound