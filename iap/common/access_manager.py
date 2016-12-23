from iap.repository.db.models_access import User, Feature, Role, Tool
from iap.repository.db.warehouse import Entity
from ..common.helper import send_success_response, send_error_response
from iap.common.security import get_user,check_session
from pyramid.interfaces import IAuthorizationPolicy
from zope.interface import implementer


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
            if request.check_access(user_id, responsibility):
                return f(request)
        else:
            return send_error_response('Unauthorised')
    return deco


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

    def check_access(self, request, user_id, responsibility):
        user = request.dbsession.query(User).filter(User.id == user_id).one()
        feature = request.dbsession.query(Feature).filter(Feature.name == responsibility).one()
        feature_id = feature.id
        tools_id = feature.tool_id
        return self.check_feature_permission(user_id, tools_id, feature_id)



