from pyramid.session import SignedCookieSessionFactory
from iap.repository.db.models_access import User
from iap.repository.db.warehouse import Entity
import jwt

my_session_factory = SignedCookieSessionFactory('itsaseekreet')


class AccessManager:
    """Access Manager that control right for
    data and functionality
    """
    def __init__(self, req):
        """Initialisation
        :param req:
        :type req:
        """
        self.request = req
        self.features = []
        self.tools = []
        self.entities = []

    def get_entity_data_access(self, user_id, tool_id, path, *kwarg):
        """
        :return:
        :rtype:
        """
        pass

    def get_user_entities(self, user_id, tool_id):
        """Get user entities

        :return:
        :rtype:
        """
        entities = []
        user = self.request.dbsession.query(User).filter(User.id == user_id).one()
        for group in user.groups:
            entity = self.request.dbsession.query(Entity).filter(Entity.id == group.id).one()
            entities.append(group.id)
        return entities

    def check_data_permission(self,user_id, group_id, entity_id):
        pass

    def check_feature_permission(self, user_id, tool_id, feature_id):
        """Boolean function that check whether user have specific
        right for tools  and features

        :return:
        :rtype:
        """
        user = self.request.dbsession.query(User).filter(User.id == user_id).one()
        features = []
        tools = []
        for role in user.roles:
            tools.append(role.tool_id)
            for feature in role.features:
                features.append(feature.id)
        if tool_id in tools and feature_id in features:
            return True
        else:
            return False


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
    config.set_session_factory(my_session_factory)





