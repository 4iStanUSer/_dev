from . import service
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Authenticated
from pyramid.security import Allow
my_session_factory = SignedCookieSessionFactory('itsaseekreet')
from iap.repository.db.models_access import User


def authorise(request):
    """Authorise function that check correctness of user password

    :param request:
    :type request:
    :return bool:
    :rtype:

    """
    try:
        login = request.json_body['login']
        password = request.json_body['password']
    except:
        return Exception
    else:
        try:
            user = request.dbsession.query(User).filter(User.email == login).one()
            #user = service.check_password(login, password)
            return user
        except:
            return Exception


def check_session(request):
    """

    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: int
    """
    #add exception on non existen  id,login in token
    session = request.session
    if 'token' in session:
        if request.headers['X-Token'] == session['token']:
            return True
        else:
            return False
    return False


def get_user(request):
    """

    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: int
    """
    #add exception on non existen  id,login in token

    try:
        user_id = request.unauthenticated_userid
        login = request.jwt_claims['login']
    except:
        return Exception
    else:
        try:
            user = request.dbsession.query(User).filter(User.id == user_id and User.email == login).one()
            #user = service.get_user_by_id(request,user_id, login)
            return user
        except:
            return Exception


def includeme(config):
    settings = config.get_settings()
    config.set_session_factory(my_session_factory)
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(authorise, 'user', reify=True)
    config.add_request_method(check_session, 'user', reify=True)