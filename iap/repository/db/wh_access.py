"""
Module for work with access entities
"""
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased

from ..warehouse import models_access as mdls

# from sqlalchemy.sql.expression import func
# from ...repository import exceptions as ex


def _get_tool_model(tool_name, model):
    return mdls.PERMS_MODELS_MAP[tool_name.lower()][model.lower()]

def get_default_perms_to_tool(sess, tool):
    _n = aliased(_get_tool_model(tool.name, 'node'))
    _np = aliased(_get_tool_model(tool.name, 'node'))
    _v = aliased(_get_tool_model(tool.name, 'value'))

    query = sess.query(_v.user_id.label("user_id"),
                       _n.id.label("node_id"),
                       _np.id.label("parent_node_id"),
                       _v.value.label('mask'),
                       _n.node_type) \
        .outerjoin(_np, _n.parents) \
        .outerjoin(_v, _n.perm_values) \
        .filter(and_(_v.user_id == None)) \
        .group_by(_n.id)

    perms = query.all()

    return perms

def get_user_perms_to_tool(sess, tool, user):
    _n = aliased(_get_tool_model(tool.name, 'node'))
    _np = aliased(_get_tool_model(tool.name, 'node'))
    _v = aliased(_get_tool_model(tool.name, 'value'))

    query = sess.query(_v.user_id.label("user_id"),
                       _n.id.label("node_id"),
                       _np.id.label("parent_node_id"),
                       _v.value.label('mask'),
                       _n.node_type) \
        .outerjoin(_np, _n.parents) \
        .outerjoin(_v, _n.perm_values) \
        .filter(and_(_v.user_id == user.id)) \
        .group_by(_n.id)

    perms = query.all()

    return perms


def get_user_features_to_tool(sess, tool, user):
    return sess.query(mdls.Feature) \
        .join(mdls.Tool, mdls.Feature.tool) \
        .join(mdls.Role, mdls.Feature.roles) \
        .join(mdls.User, mdls.Role.users) \
        .filter(and_(mdls.Tool.id == tool.id,
                     mdls.User.id == user.id)) \
        .all()


def get_role_by_id(sess, role_id):
    return sess.query(mdls.Role).get(role_id)


def get_role_by_name(sess, name):
    return sess.query(mdls.Role).filter(mdls.Role.name == name).one_or_none()


def get_tool_by_id(sess, tool_id):
    return sess.query(mdls.Tool).get(tool_id)


def get_tool_by_name(sess, name):
    return sess.query(mdls.Tool).filter(mdls.Tool.name == name).one_or_none()


def add_role(sess, name):  # , client=None, tool=None
    new_role = mdls.Role(name=name)
    sess.add(new_role)
    return new_role


def add_role_to_tool(sess, role, tool):
    return tool.roles.append(role)


def add_user(sess, email, password, role=None):
    new_user = mdls.User(email=email, password=password)
    if role is None:
        sess.add(new_user)
    else:
        role.users.append(new_user)
    return new_user


def add_role_to_user(sess, user, role):
    return user.roles.append(role)


def get_user_by_id(sess, user_id):
    return sess.query(mdls.User).get(user_id)


def get_user_by_email(sess, email):
    return sess.query(mdls.User).filter(mdls.User.email == email).one_or_none()


def get_feature_by_id(sess, feature_id):
    return sess.query(mdls.Feature).get(feature_id)


def get_feature_by_name_in_tool(sess, name, tool):
    features = tool.features
    for feature in features:
        if feature.name == name:
            return feature
    return None


def get_feature_by_name_in_role(sess, name, role):
    features = role.features
    for feature in features:
        if feature.name == name:
            return feature
    return None


def add_tool(sess, name):
    new_tool = mdls.Tool(name=name)
    sess.add(new_tool)
    return new_tool


def add_role_to_tool(sess, role, tool):
    return tool.roles.append(role)


def add_feature(sess, name, tool=None, role=None):
    new_feature = mdls.Feature(name=name)
    added = False
    if tool is not None:
        tool.features.append(new_feature)
        added = True
    if role is not None:
        role.features.append(new_feature)
        added = True

    if not added:
        sess.add(new_feature)

    return new_feature


def add_feature_to_tool(sess, feature, tool):
    return tool.features.append(feature)


def add_feature_to_role(sess, role, feature):
    return role.features.append(feature)


def add_perm_node(sess, tool, node_type, parent=None):
    node_model = _get_tool_model(tool.name, 'node')
    new_node = node_model(node_type=node_type)
    if parent is not None:
        parent.children.append(new_node)
    else:
        sess.add(new_node)

    return new_node


def get_perm_node_in_tool(sess, node_id, tool):
    node_model = _get_tool_model(tool.name, 'node')
    return sess.query(node_model).filter(node_model.id == node_id) \
        .one_or_none()


def add_perm_value(sess, tool, perm_node, value, user):
    value_model = _get_tool_model(tool.name, 'value')

    new_perm_value = value_model(value=value, user_id=user.id)
    perm_node.perm_values.append(new_perm_value)
    return new_perm_value


def add_default_perm_value(sess, tool, perm_node, value):
    value_model = _get_tool_model(tool.name, 'value')

    new_perm_value = value_model(value=value)
    perm_node.perm_values.append(new_perm_value)
    return new_perm_value


########################################################

# def add_perms_to_role(self, role, permissions):
#     if role is None:
#         raise ex.EmptyInputsError('role')
#     role.feature_permissions.extend(permissions)
#     self.db.session.commit()
#     return role
#
#
# def get_role_perms(self, role):
#     if role is None:
#         raise ex.EmptyInputsError('role')
#     return role.feature_permissions
#
#
# def delete_role_perms(self, role, permissions):
#     '''Attributes
#     role - object
#     permissions - id
#     '''
#     if role is None:
#         raise ex.EmptyInputsError('role')
#     if len(permissions) == 0:
#         raise ex.WrongArgsError('delete_role_perms')
#     if len(role.feature_permissions) == 0:
#         raise ex.NotExistsError('Role.feature_permissions',
#                                 'feature_permissions',
#                                 'feature_permissions')
#     need_commit = False
#     for id in permissions:
#         del_index = -1
#         for i in len(role.feature_permissions):
#             if role.feature_permissions[i].id == id:
#                 del_index = i
#                 need_commit = True
#         if del_index >= 0:
#             del role.feature_permissions[del_index]
#         else:
#             raise ex.NotExistsError('FeaturePermission', 'id', id)
#     if need_commit:
#         self.db.session.commit()
#     else:
#         raise ex.NoCnahgesError('FeaturePermission', 'delete_role_perms')
#
#
# def update_role_perms(self, role, permissions):
#     '''Attributes
#     role - object
#     permissions - feature_permissions_ids
#     '''
#     need_commit = False
#     if role is None:
#         raise ex.EmptyInputsError('role')
#     if not isinstance(permissions, list):
#         raise ex.EmptyInputsError('FeaturePermission')
#     if len(permissions) == 0:
#         raise ex.EmptyInputsError('FeaturePermission')
#     # delete
#     ids_to_del = []
#     for perm in role.feature_permissions:
#         is_matched = False
#         for item_id in permissions:
#             if perm.id == item_id:
#                 is_matched = True
#                 break
#         if not is_matched:
#             ids_to_del.append(perm.id)
#     # add
#     to_add_ids = []
#     for new_id in permissions:
#         is_not_found = True
#         for perm in role.feature_permissions:
#             if perm.id == new_id:
#                 is_not_found = False
#                 break
#         if is_not_found:
#             to_add_ids.append(new_id)
#     # apply changes
#     if len(ids_to_del) > 0:
#         for id in ids_to_del:
#             del_index = -1
#             for i in range(len(role.feature_permissions)):
#                 if role.feature_permissions[i].id == id:
#                     del_index = i
#                     need_commit = True
#                     break
#             if del_index >= 0:
#                 del role.feature_permissions[del_index]
#                 # need_commit = True
#     if len(to_add_ids) > 0:
#         objects_to_add = self.db.session.query(FeaturePermission) \
#             .filter(FeaturePermission.id.in_(to_add_ids))
#         role.feature_permissions.extend(objects_to_add)
#         need_commit = True
#     if need_commit:
#         self.db.session.commit()
#         return role
#     else:
#         class_name = existed_feature.__class__.__name__
#         raise ex.NoCnahgesError(class_name, 'update_role_perms')
#
#
# def update_user_roles(self, user_id, roles_id):
#     '''
#     user_id - id
#     roles_id - list of roles id
#     '''
#     user = self.warh_common.get_user(id=user_id)
#     user_roles = user.roles
#     # items to delete
#     ids_to_delete = []
#     for role in user_roles:
#         is_not_found = True
#         for new_id in roles_id:
#             if role.id == new_id:
#                 is_not_found = False
#                 break
#         if is_not_found:
#             ids_to_delete.append(role.id)
#     # add
#     to_add_ids = []
#     for new_id in roles_id:
#         is_not_found = True
#         for role in user_roles:
#             if role.id == new_id:
#                 is_not_found = False
#                 break
#         if is_not_found:
#             to_add_ids.append(new_id)
#     # apply changes
#     if len(ids_to_delete) > 0:
#         for id in ids_to_delete:
#             del_index = -1
#             for i in range(len(user_roles)):
#                 if user_roles[i].id == id:
#                     del_index = i
#                     need_commit = True
#                     break
#             if del_index >= 0:
#                 del user_roles[del_index]
#     if len(to_add_ids) > 0:
#         obj_list = []
#         for id in to_add_ids:
#             role_obj = self.warh_common.get_role(id=id)
#             if role_obj is None:
#                 raise ex.NotExistsError('Role', 'id', id)
#             obj_list.append(role_obj)
#             need_commit = True
#         user.roles.extend(obj_list)
#     if need_commit:
#         self.db.session.commit()
#         return user
#     else:
#         class_name = user.__class__.__name__
#         raise ex.NoCnahgesError(class_name, 'update_user_roles')

######################################

# class WarehouseAccess:
#     """
#     Class for user roles management.
#     """
#     def __init__(self, db_connector, warh_common):
#         self.db = db_connector
#         self.warh_common = warh_common
#
#     # region Role permissions
#     def add_perms_to_role(self, role, permissions):
#         if role is None:
#             raise ex.EmptyInputsError('role')
#         role.feature_permissions.extend(permissions)
#         self.db.session.commit()
#         return role
#
#     def get_role_perms(self, role):
#         if role is None:
#             raise ex.EmptyInputsError('role')
#         return role.feature_permissions
#
#     def delete_role_perms(self, role, permissions):
#         '''Attributes
#         role - object
#         permissions - id
#         '''
#         if role is None:
#             raise ex.EmptyInputsError('role')
#         if len(permissions) == 0:
#             raise ex.WrongArgsError('delete_role_perms')
#         if len(role.feature_permissions) == 0:
#             raise ex.NotExistsError('Role.feature_permissions',
#                                     'feature_permissions',
#                                     'feature_permissions')
#         need_commit = False
#         for id in permissions:
#             del_index = -1
#             for i in len(role.feature_permissions):
#                 if role.feature_permissions[i].id == id:
#                     del_index = i
#                     need_commit = True
#             if del_index >= 0:
#                 del role.feature_permissions[del_index]
#             else:
#                 raise ex.NotExistsError('FeaturePermission', 'id', id)
#         if need_commit:
#             self.db.session.commit()
#         else:
#             raise ex.NoCnahgesError('FeaturePermission', 'delete_role_perms')
#
#     def update_role_perms(self, role, permissions):
#         '''Attributes
#         role - object
#         permissions - feature_permissions_ids
#         '''
#         need_commit = False
#         if role is None:
#             raise ex.EmptyInputsError('role')
#         if not isinstance(permissions, list):
#             raise ex.EmptyInputsError('FeaturePermission')
#         if len(permissions) == 0:
#             raise ex.EmptyInputsError('FeaturePermission')
#         #delete
#         ids_to_del = []
#         for perm in role.feature_permissions:
#             is_matched = False
#             for item_id in permissions:
#                 if perm.id == item_id:
#                     is_matched = True
#                     break
#             if not is_matched:
#                 ids_to_del.append(perm.id)
#         #add
#         to_add_ids = []
#         for new_id in permissions:
#             is_not_found = True
#             for perm in role.feature_permissions:
#                 if perm.id == new_id:
#                     is_not_found = False
#                     break
#             if is_not_found:
#                 to_add_ids.append(new_id)
#         #apply changes
#         if len(ids_to_del) > 0:
#             for id in ids_to_del:
#                 del_index = -1
#                 for i in range(len(role.feature_permissions)):
#                     if role.feature_permissions[i].id == id:
#                         del_index = i
#                         need_commit = True
#                         break
#                 if del_index >= 0:
#                     del role.feature_permissions[del_index]
#             #need_commit = True
#         if len(to_add_ids) > 0:
#             objects_to_add = self.db.session.query(FeaturePermission)\
#                 .filter(FeaturePermission.id.in_(to_add_ids))
#             role.feature_permissions.extend(objects_to_add)
#             need_commit = True
#         if need_commit:
#             self.db.session.commit()
#             return role
#         else:
#             class_name = existed_feature.__class__.__name__
#             raise ex.NoCnahgesError(class_name, 'update_role_perms')
#
#     def update_user_roles(self, user_id, roles_id):
#         '''
#         user_id - id
#         roles_id - list of roles id
#         '''
#         user = self.warh_common.get_user(id=user_id)
#         user_roles = user.roles
#         #items to delete
#         ids_to_delete = []
#         for role in user_roles:
#             is_not_found = True
#             for new_id in roles_id:
#                 if role.id == new_id:
#                     is_not_found = False
#                     break
#             if is_not_found:
#                 ids_to_delete.append(role.id)
#         #add
#         to_add_ids = []
#         for new_id in roles_id:
#             is_not_found = True
#             for role in user_roles:
#                 if role.id == new_id:
#                     is_not_found = False
#                     break
#             if is_not_found:
#                 to_add_ids.append(new_id)
#         #apply changes
#         if len(ids_to_delete) > 0:
#             for id in ids_to_delete:
#                 del_index = -1
#                 for i in range(len(user_roles)):
#                     if user_roles[i].id == id:
#                         del_index = i
#                         need_commit = True
#                         break
#                 if del_index >= 0:
#                     del user_roles[del_index]
#         if len(to_add_ids) > 0:
#             obj_list = []
#             for id in to_add_ids:
#                 role_obj = self.warh_common.get_role(id=id)
#                 if role_obj is None:
#                     raise ex.NotExistsError('Role', 'id', id)
#                 obj_list.append(role_obj)
#                 need_commit = True
#             user.roles.extend(obj_list)
#         if need_commit:
#             self.db.session.commit()
#             return user
#         else:
#             class_name = user.__class__.__name__
#             raise ex.NoCnahgesError(class_name, 'update_user_roles')
#     # endregion Role permissions
#
#
#     # def update_role_access(self, role, entity, point, level):
#     #     if role is None:
#     #         raise ex.EmptyInputsError('role')
#     #     elif entity is None:
#     #         raise ex.EmptyInputsError('entity')
#     #     elif point is None:
#     #         raise ex.EmptyInputsError('point')
#     #     elif level is None:
#     #         raise ex.EmptyInputsError('level')
