from iap.repository.db.models_access import User
from iap.repository.db.warehouse import Entity
from ..common.helper import send_success_response, send_error_response
from iap.common.security import get_user


def check_permission(f):
    """Decorator that check if user is authorisaed and
     allow to continue view function execution in succcesive case
    :param f:
    :type f:
    :return:
    :rtype:

    """
    def deco(request):
        user_id = get_user(request)
        responsibility = request.current_route_path()
        if user_id != Exception and check_session(request) == True:
            #To do realise check access
            if check_access(user_id, responsibility):
                return f(request)
        else:
            return send_error_response('Unauthorised')
    return deco




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
        self.roles = []
        self.user_groups=[]
        self.tools = []
        self.entities = []

    def fill_attributes(self, request):
        """Fill attributes of accces rights

        :return:
        :rtype:
        """
        user_id = request.get_user.id
        user = self.request.dbsession.query(User).filter(User.id == user_id).one()
        for group in user.groups:
            self.user_groups.append(group.id)

        for role in user.roles:
            self.tools.append(role.tool_id)
            for feature in role.features:
                self.features.append(feature.id)
                self.tool.append(feature.tool_id)

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
        for role in user.roles:
            self.tools.append(role.tool_id)
            for feature in role.features:
                self.features.append(feature.id)
        if tool_id in self.tools and feature_id in self.features:
            return True
        else:
            return False
