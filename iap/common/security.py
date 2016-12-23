from pyramid.session import SignedCookieSessionFactory
from iap.repository.db.models_access import User
from iap.repository.db.warehouse import Entity
import jwt

my_session_factory = SignedCookieSessionFactory('itsaseekreet')


def authorise(req):
    """Authorise function that check correctness of user password
        # user.check_password(password)
        # user = service.check_password(login, password)
    """

    try:
        username = req.json_body['username']
        password = req.json_body['password']
        user = req.dbsession.query(User).filter(User.email == username).one()
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
    #   add exception on non existen  id,login in token
    session = request.session
    if 'token' in session:
        if request.json_body['X-Token'] == session['token']:
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
        token = request.json_body['X-Token']
        token_data = jwt.decode(token, 'secret', algorithms=['HS512'])
        user_id = token_data['sub']
        login = token_data['login']
        user = request.dbsession.query(User).filter(User.id == user_id and User.email == login).one()
        # user = service.get_user_by_id(request,user_id, login)
        return user
    except:
        return Exception


def includeme(config):
    settings = config.get_settings()
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(check_session, 'has_session', reify=True)
    config.add_request_method(authorise, 'autorised', reify=True)
    config.set_session_factory(my_session_factory)





