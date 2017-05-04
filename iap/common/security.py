from pyramid.session import SignedCookieSessionFactory
from sqlalchemy.orm.exc import NoResultFound
from ..common.helper import send_error_response
from iap.common.repository.models.access import User
from .exceptions import IncorrectPassword
from pyramid.interfaces import IAuthorizationPolicy
from zope.interface import implementer
from .exceptions import *
from functools import wraps
import jwt
import pyramid.httpexceptions as http_exc

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
        try:
            user_id = get_user(request)
            issession = check_session(request)
            if user_id!=None and issession==True:
                return f(request)
        except WrongRequestMethod:
            raise http_exc.HTTPBadRequest()
            # msg = request.get_error_msg('RequestError')
            # return send_error_response(msg)
        except NoResultFound:
            raise http_exc.HTTPNotFound()
            # msg = request.get_error_msg('NoResultFound')
            # return send_error_response(msg)
        except KeyError:
            raise http_exc.HTTPUnauthorized()
            # msg = request.get_error_msg('Unauthorised')
            # return send_error_response(msg)
        except AttributeError:
            raise http_exc.HTTPUnauthorized()
            # msg = request.get_error_msg('Unauthorised')
            # return send_error_response(msg)
        except jwt.exceptions.DecodeError:
            msg = request.get_error_msg('TokenError')
            return send_error_response(msg)
    return deco



def authorise(session, user_name, password):
    """Authorise function that check user existense
        # user.check_password(password)
        # user = service.check_password(login, password)
    """
    try:
        user = session.query(User).filter(User.email == user_name).one()
    except NoResultFound:
        raise NoResultFound
    except AttributeError:
        raise AttributeError
    except TypeError:
        raise TypeError
    else:
        if user.check_password(password):
            return user.id, user.email
        else:
            raise IncorrectPassword


def check_session(request):
    """

    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: int
    """
    #   add exception on non existen  id,login in token
    try:
        session = request.session
        if 'token' in session:
            if request.headers.get('X-Token') == session['token']:  # request.json['X-Token']
                return True
            else:
                return True#TODO change on False
    except JSONDecodeError:
        raise WrongRequestMethod
    except AttributeError:
        return True
    except KeyError:
        raise KeyError
    else:
        return True



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
        token = request.headers.get('X-Token').split()  # request.json['X-Token']
        if len(token) > 1:
            token = token[1]
        token_data = jwt.decode(token, 'secret', algorithms=['HS512'])

        user_id = int(token_data['sub'])  # int(request.jwt_claims['sub'])
        login = token_data['login']  # request.jwt_claims['login']
        user = request.dbsession.query(User).filter(User.id == user_id and User.email == login).one()
        # user = service.get_user_by_id(request,user_id, login)
    except JSONDecodeError:
        raise WrongRequestMethod
    except NoResultFound:
        raise http_exc.HTTPNotFound
    except jwt.exceptions.DecodeError:
        raise http_exc.HTTPNotFound
    except KeyError:
        raise KeyError
    except Exception:
        raise Exception
    else:
        return user.id


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
            user_id = request.user
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










