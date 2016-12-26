from pyramid.session import SignedCookieSessionFactory
from ..common.helper import send_error_response
from iap.repository.db.models_access import User
from iap.repository.db.warehouse import Entity
from pyramid.interfaces import IAuthorizationPolicy
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
        if user_id != Exception and check_session(request) == True:
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
        username = req.json_body['username']
        password = req.json_body['password']
        user = req.dbsession.query(User).filter(User.email == username).one()
        #TO DO add check password
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


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(request):
            user = get_user(request)
            if request.check_access(user.id, roles) == False:
                return send_error_response("User {0} Unauthorised".format(user.id))
            return f(request)
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
        self.features = []
        self.roles = []
        self.user_groups=[]
        self.tools = []
        self.entities = []

    def permits(self, context, identity, permission):
        """ Return True if the userid is allowed the permission in the
                  current context, else return False"""
        pass

    def authorized_userid(self, identity):
        """ Return the userid of the user identified by the identity
                  or 'None' if no user exists related to the identity """
        pass

    def get_entity_data_access(self, request, user_id, tool_id, path, *kwarg):
        """
        :return:
        :rtype:
        """
        pass


    def get_user_entities(self, request, user_id, tool_id):
        """Get user entities

        :return:
        :rtype:
        """
        entities = []
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        for group in user.groups:
            entity = request.dbsession.query(Entity).filter(Entity.id == group.id).one()
            entities.append(entity.id)
        return entities

    def check_data_permission(self, request, user_id, group_id, entity_id):
        """
        Check data permission

        :param request:
        :type request:
        :param user_id:
        :type user_id:
        :param group_id:
        :type group_id:
        :param entity_id:
        :type entity_id:
        :return:
        :rtype:
        """
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        for group in user.roles:
            self.groups.append(group.id)
        if entity_id in self.groups:
            return True
        else:
            return False

    def check_feature_permission(self, request,user_id, tool_id, feature_id):
        """Boolean function that check whether user have specific
        right for tools  and features

        :return:
        :rtype:
        """
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        for role in user.roles:
            self.tools.append(role.tool_id)
            for feature in role.features:
                self.features.append(feature.id)
        if tool_id in self.tools and feature_id in self.features:
            return True
        else:
            return False

    def _check_access(self,request, user_id, roles):
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        roles_names  = [role.name for role in user.roles]
        if list(set(roles_names) & set(roles)) != []:
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
    config.add_request_method(authorise, 'autorised', reify=True)
    config.set_session_factory(my_session_factory)



