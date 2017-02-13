from pyramid.session import SignedCookieSessionFactory
from sqlalchemy.orm.exc import NoResultFound
from ..common.helper import send_error_response
from iap.common.repository.models.access import User, DataPermissionAccess, Role, Feature
from iap.common.repository.models.warehouse import Entity
from pyramid.interfaces import IAuthorizationPolicy
from .error_manager import ErrorManager
from zope.interface import implementer
from functools import wraps
import jwt

my_session_factory = SignedCookieSessionFactory('itsaseekreet')


def forbidden_view(f):
    """Decorator that check if user is authentificated and
     allow to continue view function execution in succcesive case
    :param f:
    :type f:
    :return:
    :rtype:

    """
    def deco(request):
        user_id = get_user(request)
        if user_id!=None and check_session(request)==True:
            return f(request)
        else:
            return send_error_response('Unauthorised')
    return deco


def authorise(req):
    """Authorise function that check user existense
        # user.check_password(password)
        # user = service.check_password(login, password)
    """
    try:
        username = req.json_body['data']['username']
        password = req.json_body['data']['password']
        user = req.dbsession.query(User).filter(User.email == username).one()
    except NoResultFound:
        return None
    else:
        if user.check_password(password):
            return user
        else:
            return None


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
    Return user decoding token

    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: int
    """
    #add exception on non existen  id,login in token
    try:
        token = request.json_body['X-Token']
        token_data = jwt.decode(token, 'secret', algorithms=['HS512'])
        user_id = int(token_data['sub'])
        login = token_data['login']
        user = request.dbsession.query(User).filter(User.id == user_id and User.email == login).one()
        # user = service.get_user_by_id(request,user_id, login)
    except NoResultFound:
        return 2#TODO change on None
    except jwt.exceptions.DecodeError:
        return 2#TODO change on None
    except KeyError:
        return None
    else:
        return 2#TODO change on None user.id


def requires_roles(*roles):
    """
    Decorator that wrap around view function
    Check permission access for specific view function

    :param roles:
    :type roles:
    :return:
    :rtype: function
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(request):
            user_id = get_user(request)
            if request.check_access(user_id, roles):
                return f(request)
            else:
                return send_error_response("User {0} Unauthorised".format(user_id))
        return wrapped
    return wrapper


@implementer(IAuthorizationPolicy)
class AccessManager:
    """Access Manager that control right for
    data and functionality
    """
    def __init__(self):
        """Initialisaion
        :param req:
        :type req:
        """

    def permits(self, context, identity, permission):
        """ Return True if the userid is allowed the permission in the
                  current context, else return False"""
        pass

    def authorized_userid(self, identity):
        """ Return the userid of the user identified by the identity
                  or 'None' if no user exists related to the identity """
        pass


    def _check_access(self, request, user_id, in_features):
        """
        Verify if specific user has specific role
        :param request:
        :type request: pyramid.util.Request
        :param user_id:
        :type user_id: int
        :param roles:
        :type roles: Tuple
        :return:
        :rtype: bool
        """
        try:
            user = request.dbsession.query(User).filter(User.id == user_id).one()
            features = []
            for role in user.roles:
                for feature in role.features:
                    features.append(feature.name)
        except NoResultFound:
            return False
        else:
            if list(set(in_features) & set(features)) != []:
                return True
            else:
                return False


def set_manager(config):
    """
    Durective set manager

    :param config:
    :type config:
    :return:
    :rtype:
    """
    policy = AccessManager()

    def check_access(request, user_id, roles):
        return policy._check_access(request, user_id, roles)

    config.set_authorization_policy(policy)
    config.add_request_method(check_access, 'check_access')


def includeme(config):

    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(check_session, 'has_session', reify=True)
    config.add_request_method(authorise, 'authorised', reify=True)
    config.set_session_factory(my_session_factory)










