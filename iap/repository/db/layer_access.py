"""
Module for work with access
"""
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from iap.repository.db import models_access as mdls


def _get_tool_model(tool_name, model):
    return mdls.PERMS_MODELS_MAP[tool_name.lower()][model.lower()]


def get_perms_to_tool(ssn, tool, user=None):
    _n = aliased(_get_tool_model(tool.name, 'node'))
    _np = aliased(_get_tool_model(tool.name, 'node'))
    _v = aliased(_get_tool_model(tool.name, 'value'))

    user_id = None if user is None else user.id
    query = ssn.query(_v,
                      _n,
                      _v.user_id.label("user_id"),
                      _v.value.label('mask'),
                      _n.name.label("node_name"),
                      _n.node_type.label("node_type"),
                      _n.id.label("node_id"),
                      _np.id.label("parent_node_id")) \
        .outerjoin(_n) \
        .outerjoin(_np, _n.parents) \
        .filter(and_(_v.user_id.is_(user_id)))

    perms = query.all()

    permissions = []
    if perms is not None:
        for ind, perm in enumerate(perms):
            node_parents = _get_all_perm_node_parents(perm[1])
            if node_parents is not None:
                node_parents.reverse()
                node_parents = [x.name for x in node_parents]
            else:
                node_parents = []

            permissions.append({
                'name': perm.node_name,
                'user_id': perm.user_id,
                'mask': perm.mask,
                'path': node_parents,
                'node_type': perm.node_type
            })

    return permissions


def _get_all_perm_node_parents(perm_node, include_this=False):
    parents = []
    if perm_node is not None:
        if include_this:
            parents.append(perm_node)
        if perm_node.parents and len(perm_node.parents):
            # TODO WARN
            p = _get_all_perm_node_parents(perm_node.parents[0], True)
            if p and len(p):
                parents.extend(p)
        return parents
    return None


# def get_user_perms_to_tool(ssn, tool, user):
#     _n = aliased(_get_tool_model(tool.name, 'node'))
#     _np = aliased(_get_tool_model(tool.name, 'node'))
#     _v = aliased(_get_tool_model(tool.name, 'value'))
#
#     query = ssn.query(_v.user_id.label("user_id"),
#                        _n.id.label("node_id"),
#                        _np.id.label("parent_node_id"),
#                        _v.value.label('mask'),
#                        _n.node_type) \
#         .outerjoin(_np, _n.parents) \
#         .outerjoin(_v, _n.perm_values) \
#         .filter(and_(_v.user_id == user.id)) \
#         .group_by(_n.id)
#
#     perms = query.all()
#
#     return perms


def get_user_features_to_tool(ssn, tool, user):
    return ssn.query(mdls.Feature) \
        .join(mdls.Tool, mdls.Feature.tool) \
        .join(mdls.Role, mdls.Feature.roles) \
        .join(mdls.User, mdls.Role.users) \
        .filter(and_(mdls.Tool.id == tool.id,
                     mdls.User.id == user.id)) \
        .all()


def get_role_by_id(ssn, role_id):
    return ssn.query(mdls.Role).get(role_id)


def get_role_by_name(ssn, name):
    return ssn.query(mdls.Role).filter(mdls.Role.name == name).one_or_none()


def get_tool_by_id(ssn, tool_id):
    return ssn.query(mdls.Tool).get(tool_id)


def get_tool_by_name(ssn, name):
    return ssn.query(mdls.Tool).filter(mdls.Tool.name == name).one_or_none()


def add_role(ssn, name):  # , client=None, tool=None
    new_role = mdls.Role(name=name)
    ssn.add(new_role)
    return new_role


# def add_role_to_tool(ssn, role, tool):
#     return tool.roles.append(role)


def add_user(ssn, email, password, roles=None):
    new_user = mdls.User(email=email, password=password)
    if roles is None:
        ssn.add(new_user)
    else:
        for role in roles:
            role.users.append(new_user)
    return new_user


def add_role_to_user(ssn, user, role):
    return user.roles.append(role)


def add_tool(ssn, name):
    new_tool = mdls.Tool(name=name)
    ssn.add(new_tool)
    return new_tool


def add_role_to_tool(ssn, role, tool):
    return tool.roles.append(role)


def add_feature(ssn, name, tool=None, role=None):
    new_feature = mdls.Feature(name=name)
    added = False
    if tool is not None:
        tool.features.append(new_feature)
        added = True
    if role is not None:
        role.features.append(new_feature)
        added = True

    if not added:
        ssn.add(new_feature)

    return new_feature


def add_feature_to_tool(ssn, feature, tool):
    return tool.features.append(feature)


def add_feature_to_role(ssn, role, feature):
    return role.features.append(feature)


def add_perm_node(ssn, tool, node_type, name, parent=None):
    node_model = _get_tool_model(tool.name, 'node')
    new_node = node_model(node_type=node_type, name=name)
    if parent is not None:
        parent.children.append(new_node)
    else:
        ssn.add(new_node)

    return new_node


def get_perm_node_in_tool(ssn, node_id, tool):
    node_model = _get_tool_model(tool.name, 'node')
    return ssn.query(node_model).filter(node_model.id == node_id) \
        .one_or_none()


def add_perm_value(ssn, tool, perm_node, value, user):
    value_model = _get_tool_model(tool.name, 'value')

    new_perm_value = value_model(value=value, user_id=user.id)
    perm_node.perm_values.append(new_perm_value)
    return new_perm_value


def add_default_perm_value(ssn, tool, perm_node, value):
    value_model = _get_tool_model(tool.name, 'value')

    new_perm_value = value_model(value=value)
    perm_node.perm_values.append(new_perm_value)
    return new_perm_value


# region Users methods

def get_user_by_id(ssn, user_id):
    return ssn.query(mdls.User).get(user_id)


def get_user_by_email(ssn, email):
    return ssn.query(mdls.User).filter(mdls.User.email == email).one_or_none()


def get_users_by_tool(ssn, tool):
    return ssn.query(mdls.User) \
        .join(mdls.Role, mdls.User.roles) \
        .join(mdls.Tool, mdls.Role.tool_id) \
        .filter(and_(mdls.Tool.id == tool.id)) \
        .all()


def get_all_users(ssn):
    return ssn.query(mdls.User).all()


def get_user_role_in_tool(ssn, user, tool):
    return ssn.query(mdls.Role) \
        .join(mdls.User, mdls.Role.users) \
        .join(mdls.Tool, mdls.Role.tool_id) \
        .filter(and_(mdls.Tool.id == tool.id,
                     mdls.User.id == user.id)) \
        .one_or_none()  # TODO Question

# endregion


# region Groups methods

def add_user_group(ssn, name, tool):
    new_group = mdls.UserGroup(name=name)
    return tool.user_groups.append(new_group)

def get_user_group_by_id(ssn, group_id):
    return ssn.query(mdls.UserGroup).get(group_id)

# endregion


# region Features methods

def get_features_by_tool(ssn, tool):
    return tool.features


def add_features_to_role(ssn, role, features):
    for feature in features:
        role.append(feature)


def del_features_from_role(ssn, role, features_id):
    return ssn.query(mdls.Feature) \
        .join(mdls.Role, mdls.Feature.roles) \
        .filter(and_(mdls.Role.id.in_(features_id),
                     mdls.Role.id == role.id)) \
        .delete()


def get_feature_by_id(ssn, feature_id):
    return ssn.query(mdls.Feature).get(feature_id)


def get_feature_by_name_in_tool(ssn, name, tool):
    features = tool.features
    for feature in features:
        if feature.name == name:
            return feature
    return None


def get_feature_by_name_in_role(ssn, name, role):
    features = role.features
    for feature in features:
        if feature.name == name:
            return feature
    return None

# endregion


# region Permissions methods

def get_raw_perm_values_for_user(ssn, tool, user_id=None):
    _v = aliased(_get_tool_model(tool.name, 'value'))

    return ssn.query(_v).filter(and_(_v.user_id.is_(user_id))).all()


def get_nodes_by_name(ssn, tool, name):
    _n = aliased(_get_tool_model(tool.name, 'node'))

    return ssn.query(_n).filter(and_(_n.name == name)).all()


def del_perm_values_for_user(ssn, tool, user):
    _v = _get_tool_model(tool.name, 'value')

    results = ssn.query(_v).filter(and_(_v.user_id.is_(user.id))).all()
    for res in results:
        ssn.delete(res)

# endregion