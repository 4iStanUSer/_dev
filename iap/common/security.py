from pyramid.session import SignedCookieSessionFactory
from sqlalchemy.orm.exc import NoResultFound
from ..common.helper import send_error_response
from iap.common.repository.models.access import User
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
    print(request)
    try:
        token = request.json_body['X-Token']
        token_data = jwt.decode(token, 'secret', algorithms=['HS512'])
        user_id = int(token_data['sub'])
        login = token_data['login']
        user = request.dbsession.query(User).filter(User.id == user_id and User.email == login).one()
        # user = service.get_user_by_id(request,user_id, login)
    except NoResultFound:
        return None
    except jwt.exceptions.DecodeError:
        return None
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

    def get_entity_data_access(self, request, user_id):
        """
        Return entitie's mask
        :return:
        :rtype:
        """
        mask = []
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        for permission in user.perms:
            for dataperm in permission.data_perms:
                mask.append(dataperm.mask)
        return mask

    def get_user_entities(self, request, user_id):
        """Retunr list of dictionary - with keys
        in_path, out_path, mask

        :return:
        :rtype:
        """
        entities = []
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        for permission in user.perms:
            for data_perm in permission.data_perms:
                entities.append({'in_path':data_perm.in_path, 'out_path':data_perm.out_path, 'mask':data_perm.mask})
        return entities


    def check_feature_permission(self, request, user_id, tool_id, feature_id):
        """Boolean function that check whether user have specific
        right for tools  and features

        :return:
        :rtype:
        """
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        tools = []
        features = []
        for role in user.roles:
            tools.append(role.tool_id)
            for feature in role.features:
                features.append(feature.id)
        if tool_id in tools and feature_id in features:
            return True
        else:
            return False

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


def check_permission_for_tool_and_project(self, request, user_id, tool_id, project_id):
    """
    Function will check permission to project and tool


    :return:
    :rtype:

    """
    access = {'tool': False, 'project': False}
    user = request.dbsession.query(User).filter(User.id == user_id)
    for role in user.roles:
        if tool_id == role.tool_id:
            access['tool': True]
    for perm in user.perms:
        for data_perm in perm:
            if data_perm.project == project_id:
                access['project': True]
    if access == {'tool': True, 'project': True}:
        return True
    else:
        return False



def tree(dict, path, masks, order):
    """
    Fill tree

    :param dict:
    :type dict:
    :param path:
    :type path:
    :param order:
    :type order:
    :return:
    :rtype:
    """
    if order<len(path):
        key = path[order]
        if key not in dict.keys():
            dict[key]={}
            try:
                dict['mask']=masks[order]
            except:
                raise IndexError
        order+=1
        tree(dict[key], path, masks, order)


def build_permission_tree(request, project_name):
    """
    Build permission tree
    :return:
    :rtype:
    """

    list_of_access = []
    user_id = 2#request.user
    user = request.dbsession.query(User).filter(User.id == user_id).one()
    for perm in user.perms:
        for data_perm in perm.data_perms:
            if project_name==data_perm.project:
                perm_node = dict(out_path=data_perm.out_path, in_path=data_perm.in_path, mask=data_perm.mask)
                list_of_access.append(perm_node)

    access_rights = {}
    for node in list_of_access:
        ent = node['out_path']
        if ent not in access_rights.keys():
            access_rights[ent] = {}

        masks = node['mask'].split(",")
        items = node['in_path'].split("-")
        tree(access_rights[ent], items, masks, order=0)

    return access_rights









