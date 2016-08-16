"""
Module for work with access
"""
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from iap.repository.db import models_access as mdls


def _get_tool_model(tool_name, model):
    return mdls.PERMS_MODELS_MAP[tool_name.lower()][model.lower()]


def get_default_perms_to_tool(ssn, tool):
    _n = aliased(_get_tool_model(tool.name, 'node'))
    _np = aliased(_get_tool_model(tool.name, 'node'))
    _v = aliased(_get_tool_model(tool.name, 'value'))

    query = ssn.query(_v.user_id.label("user_id"),
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


def get_user_perms_to_tool(ssn, tool, user):
    _n = aliased(_get_tool_model(tool.name, 'node'))
    _np = aliased(_get_tool_model(tool.name, 'node'))
    _v = aliased(_get_tool_model(tool.name, 'value'))

    query = ssn.query(_v.user_id.label("user_id"),
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


def add_role_to_tool(ssn, role, tool):
    return tool.roles.append(role)


def add_user(ssn, email, password, role=None):
    new_user = mdls.User(email=email, password=password)
    if role is None:
        ssn.add(new_user)
    else:
        role.users.append(new_user)
    return new_user


def add_role_to_user(ssn, user, role):
    return user.roles.append(role)


def get_user_by_id(ssn, user_id):
    return ssn.query(mdls.User).get(user_id)


def get_user_by_email(ssn, email):
    return ssn.query(mdls.User).filter(mdls.User.email == email).one_or_none()


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


def add_perm_node(ssn, tool, node_type, parent=None):
    node_model = _get_tool_model(tool.name, 'node')
    new_node = node_model(node_type=node_type)
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
