"""
Module for work with access
"""
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from iap.common.repository.models import access as mdls
from ..models.access import *
# TODO Class implementation & ssn factory


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
    """
    Return role selected by name
    :param ssn:
    :type ssn:
    :param name:
    :type name:
    :return:
    :rtype:
    """
    return ssn.query(mdls.Role).filter(mdls.Role.name == name).one_or_none()


def get_tool_by_id(ssn, tool_id):
    """
    Return tool by id selected
    :param ssn:
    :type ssn:
    :param tool_id:
    :type tool_id:
    :return:
    :rtype:
    """
    return ssn.query(mdls.Tool).get(tool_id)


def get_tool_by_name(ssn, name):
    return ssn.query(mdls.Tool).filter(mdls.Tool.name == name).one_or_none()



def get_perm_node_in_tool(ssn, node_id, tool):
    node_model = _get_tool_model(tool.name, 'node')
    return ssn.query(node_model).filter(node_model.id == node_id) \
        .one_or_none()



# region Users methods

def get_user_by_id(ssn, user_id):
    return ssn.query(mdls.User).get(user_id)


def get_user_by_email(ssn, email):
    try:
        user = ssn.query(mdls.User).filter(mdls.User.email == email).one_or_none()
    except Exception:
        return None
    else:
        return user

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

def get_user_group_by_id(ssn, group_id):
    return ssn.query(mdls.UserGroup).get(group_id)

# endregion


# region Features methods

def get_features_by_tool(ssn, tool):
    return tool.features


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




def get_data_permission_by_group(ssn, group_id):
    """
    Return list of possible permission for input group

    :param ssn:
    :type ssn:
    :param group_id:
    :type group_id:
    :return:
    :rtype:
    """
    permissions = []
    if group_id is not None:
        group = ssn.query(mdls.Group).filter(mdls.Group.id == group_id).one()
        for perm in group.data_perm:
            permissions.append((perm.name, perm.value))
    return permissions


def get_data_permission_by_id(ssn, data_perm_id):
    """
    Return data permissison models_managers by given id
    :param ssn:
    :type ssn:
    :param data_perm_id:
    :type data_perm_id:
    :return:
    :rtype:
    """
    data_perm = ssn.query(mdls.DataPermissionAccess).\
        filter(mdls.DataPermissionAccess.id == data_perm_id).one()
    return data_perm


#Rebase method's from security  to layer access
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
                dict['mask'][key] = masks[order]
            except KeyError:
                dict['mask'] = {}
                dict['mask'][key] = masks[order]
            except:
                raise IndexError
        order+=1
        tree(dict[key], path, masks, order)


def build_permission_tree(session, project_name):
    """
    Build permission tree
    :return:
    :rtype:
    """

    list_of_access = []
    user_id = 2#request.user
    user = session.query(User).filter(User.id == user_id).one()
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


def check_permission(permission_tree, inner_path, pointer):
    try:
        item = inner_path[pointer]
        if type(item) is list or item.isdigit():
            return {'item': item, 'tree': permission_tree}
        else:
            tree = permission_tree[item]
            if pointer==0:
                mask=1
            else:
                mask = permission_tree['mask']
    except KeyError:
        return "Unavailable"
    else:
        if tree == {}:
            return {'item': item, 'tree': {":".join(inner_path[-1]): mask[item]}}
        else:
            return check_permission(tree, inner_path, pointer+1)


def get_feature_permission(session, user_id, tool_id):
    """Boolean function that check whether user have specific
    right for tools  and features

    :return:
    :rtype:
    """

    feature = session.query(Feature.name).distinct(Feature.name)
    feature = feature.join(Role.users).join(Role.features)
    features = feature.filter((User.id == user_id) & (Feature.tool_id == tool_id)).all()

    user_permission = {'create': False, 'finalize': False, 'share': False,
                       'copy': False, 'edit': False, 'delete': False}
    for feature in features:
        if feature[0] in user_permission.keys():
            user_permission[feature[0]] = True
    return user_permission


def check_feature_permission(session, user_id, tool_id, feature_id):
    """Boolean function that check whether user have specific
    right for tools  and features

    :return:
    :rtype:
    """
    user = session.query(User).filter(User.id == user_id).one()
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


def get_entity_data_access(session, user_id):
    """
    Return entitie's mask
    :return:
    :rtype:
    """
    mask = []
    user = session.query(User).filter(User.id == user_id).one()
    for permission in user.perms:
        for dataperm in permission.data_perms:
            mask.append(dataperm.mask)
    return mask


def get_user_entities(session, user_id):
    """Retunr list of dictionary - with keys
    in_path, out_path, mask

    :return:
    :rtype:
    """
    entities = []
    user = session.query(User).filter(User.id == user_id).one()
    for permission in user.perms:
        for data_perm in permission.data_perms:
            entities.append({'in_path': data_perm.in_path, 'out_path': data_perm.out_path, 'mask': data_perm.mask})
    return entities


def get_entity_data_access(session, user_id):
        """
        Return entitie's mask
        :return:
        :rtype:
        """
        mask = []
        user = session.query(User).filter(User.id == user_id).one()
        for permission in user.perms:
            for dataperm in permission.data_perms:
                mask.append(dataperm.mask)
        return mask


def get_user_entities(session, user_id):
    """Retunr list of dictionary - with keys
    in_path, out_path, mask

    :return:
    :rtype:
    """
    entities = []
    user = session.query(User).filter(User.id == user_id).one()
    for permission in user.perms:
        for data_perm in permission.data_perms:
            entities.append({'in_path': data_perm.in_path, 'out_path': data_perm.out_path, 'mask': data_perm.mask})
    return entities


def check_feature_permission(session, user_id, tool_id, feature_id):
    """Boolean function that check whether user have specific
    right for tools  and features

    :return:
    :rtype:
    """
    user = session.query(User).filter(User.id == user_id).one()
    tools = []
    features = []
    for role in user.roles:
        tools.append(role.tool_id)
        for feature in role.features:
            features.append(feature.name)
    if tool_id in tools and feature_id in features:
        return True
    else:
        return False




def check_period_perm(tree, ts_period=None, ts_point=None):

    correct_ts_period = []

    if ts_period:
        ts_period = range(int(float(ts_period[0])), int(float(ts_period[1])), 1)
    else:
        ts_period = [int(ts_point)]
    for _ts_period in [i for i in tree.keys() if i!='mask']:
        _ts_period = _ts_period.split(":")

        try:
            _ts = range(int(float(_ts_period[0])), int(float(_ts_period[1]))+1, 1)
        except IndexError:
            _ts = range(int(float(_ts_period[0])), int(float(_ts_period[0])) + 1, 1)
        correct_ts_period.extend(list(set(ts_period) & set(_ts)))
    return correct_ts_period


def check_scenario_permission(user, scenario, parameter):
    """Boolean function that check whether user have specific
    right for tools  and features

    :return:
    :rtype:
    """
    if parameter in ["status", "shared", "name", 'description']:
        if scenario.author == user.email:
            return True
    elif parameter=="favorite":
        return True
    else:
        return False