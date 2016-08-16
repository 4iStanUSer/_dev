from ...repository import exceptions as ex
from ..warehouse import wh_access as wha
from .access_service import _get_int_id_or_err


def _get_str_or_err(value, name):
    try:
        if not isinstance(value, str) or len(value) == 0:
            raise ex.WrongArgEx(name, value)
        return value
    except TypeError:
        raise ex.EmptyInputsError(name)
    except ValueError:
        raise ex.WrongArgEx(name, value)


def get_role(sess, **kwargs):
    """
    Args:
        sess
        **kwargs: id|name
    """
    if 'id' in kwargs:
        role_id = _get_int_id_or_err(kwargs['id'], 'id')
        return wha.get_role_by_id(sess, role_id)

    elif 'name' in kwargs:
        name = _get_str_or_err(kwargs['name'], 'name')
        return wha.get_role_by_name(sess, name)


def get_user(sess, **kwargs):
    """
    Args:
        sess
        **kwargs: id|email
    """
    if 'id' in kwargs:
        user_id = _get_int_id_or_err(kwargs['id'], 'id')
        return wha.get_user_by_id(sess, user_id)

    elif 'email' in kwargs:
        email = _get_str_or_err(kwargs['email'], 'email')
        return wha.get_user_by_email(sess, email)


def get_tool(sess, **kwargs):
    """
    Args:
        sess
        **kwargs: id|email
    """
    if 'id' in kwargs:
        tool_id = _get_int_id_or_err(kwargs['id'], 'id')
        return wha.get_tool_by_id(sess, tool_id)

    elif 'name' in kwargs:
        name = _get_str_or_err(kwargs['name'], 'name')
        return wha.get_tool_by_name(sess, name)


def get_feature(sess, **kwargs):  # TODO Remake - **kwargs
    """
    Args:
        sess
        **kwargs: id|name & tool_id
    """
    if 'id' in kwargs:
        feature_id = _get_int_id_or_err(kwargs['id'], 'id')
        return wha.get_feature_by_id(sess, feature_id)

    elif 'name' in kwargs and 'tool_id' in kwargs:
        name = _get_str_or_err(kwargs['name'], 'name')
        tool_id = _get_int_id_or_err(kwargs['tool_id'], 'tool_id')
        tool = wha.get_tool_by_id(sess, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)
        return wha.get_feature_by_name_in_tool(sess, name, tool)


def add_role(sess, name, tool_id=None):
    name = _get_str_or_err(name, 'name')

    tool = None
    if tool_id is not None:
        tool_id = _get_int_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(sess, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

    new_role = wha.add_role(sess, name)
    if tool is not None:
        wha.add_role_to_tool(sess, new_role, tool)

    return new_role


def add_role_to_tool(sess, role_id, tool_id):
    role_id = _get_int_id_or_err(role_id, 'id')
    tool_id = _get_int_id_or_err(tool_id, 'tool_id')

    role = wha.get_role_by_id(sess, role_id)
    if role is None:
        raise ex.NotExistsError('Role', 'id', role_id)

    tool = wha.get_tool_by_id(sess, tool_id)
    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)

    # TODO Check Existed
    return wha.add_role_to_tool(sess, role, tool)


def add_user(sess, email, password, role_id=None):
    email = _get_str_or_err(email, 'email')
    password = _get_str_or_err(password, 'password')
    role = None
    if role_id is not None:
        role_id = _get_int_id_or_err(role_id, 'id')
        role = wha.get_role_by_id(sess, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)

    existed = wha.get_user_by_email(sess, email)
    if existed is not None:
        raise ex.AlreadyExistsError('User', 'email', email)

    return wha.add_user(sess, email, password, role)


def add_role_to_user(sess, user_id, role_id):
    user_id = _get_int_id_or_err(user_id, 'id')
    role_id = _get_int_id_or_err(role_id, 'id')

    role = wha.get_role_by_id(sess, role_id)
    if role is None:
        raise ex.NotExistsError('Role', 'id', role_id)

    user = wha.get_user_by_id(sess, user_id)
    if user is None:
        raise ex.NotExistsError('User', 'id', user_id)

    return wha.add_role_to_user(sess, user, role)


def add_tool(sess, name):
    name = _get_str_or_err(name, 'name')
    existed = wha.get_tool_by_name(sess, name)
    if existed is not None:
        raise ex.AlreadyExistsError('Tool', 'name', name)
    return wha.add_tool(sess, name)


def add_feature(sess, name, tool_id=None, role_id=None):
    name = _get_str_or_err(name, 'name')
    tool = None
    if tool_id is not None:
        tool_id = _get_int_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(sess, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        existed = wha.get_feature_by_name_in_tool(sess, name, tool)
        if existed is not None:
            raise ex.AlreadyExistsError('Feature', 'name', name)

    role = None
    if role_id is not None:
        role_id = _get_int_id_or_err(role_id, 'role_id')
        role = wha.get_role_by_id(sess, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)

        existed = wha.get_feature_by_name_in_role(sess, name, role)
        if existed is not None:
            raise ex.AlreadyExistsError('Feature', 'name', name)

    return wha.add_feature(sess, name, tool, role)


def add_feature_to_tool(sess, feature_id, tool_id):
    tool_id = _get_int_id_or_err(tool_id, 'tool_id')
    feature_id = _get_int_id_or_err(feature_id, 'feature_id')

    feature = wha.get_feature_by_id(sess, feature_id)
    if feature is None:
        raise ex.NotExistsError('Feature', 'id', feature_id)

    tool = wha.get_tool_by_id(sess, tool_id)
    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)

    return wha.add_feature_to_tool(sess, feature, tool)


def add_feature_to_role(sess, feature_id, role_id):
    role_id = _get_int_id_or_err(role_id, 'tool_id')
    feature_id = _get_int_id_or_err(feature_id, 'feature_id')

    feature = wha.get_feature_by_id(sess, feature_id)
    if feature is None:
        raise ex.NotExistsError('Feature', 'id', feature_id)

    role = wha.get_role_by_id(sess, role_id)
    if role is None:
        raise ex.NotExistsError('Role', 'id', role_id)

    return wha.add_feature_to_role(sess, role, feature)


def add_permission(sess, tool_id, node_type, parent_id=None):
    tool_id = _get_int_id_or_err(tool_id, 'tool_id')
    node_type = _get_str_or_err(node_type, 'node_type')  # Defined string

    tool = wha.get_tool_by_id(sess, tool_id)
    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)

    parent = None
    if parent_id is not None:
        parent_id = _get_int_id_or_err(parent_id, 'parent_id')
        parent = wha.get_perm_node_in_tool(sess, parent_id, tool)
        if parent is None:
            raise ex.NotExistsError('PermNode', 'id', parent_id)

    return wha.add_perm_node(sess, tool, node_type, parent)


def add_permission_value(sess, tool_id, perm_node_id, value, user_id):
    tool_id = _get_int_id_or_err(tool_id, 'tool_id')
    perm_node_id = _get_int_id_or_err(perm_node_id, 'perm_node_id')
    user_id = _get_int_id_or_err(user_id, 'user_id')

    tool = wha.get_tool_by_id(sess, tool_id)
    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)

    user = wha.get_user_by_id(sess, user_id)
    if user is None:
        raise ex.NotExistsError('User', 'id', user_id)

    perm_node = wha.get_perm_node_in_tool(sess, perm_node_id, tool)
    if perm_node is None:
        raise ex.NotExistsError('PermNode', 'id', perm_node_id)

    return wha.add_perm_value(sess, tool, perm_node, value, user)


def init_permissions(sess, tool_id, structure):
    if 'permissions' not in structure or \
            not isinstance(structure['permissions'], list):
        raise ex.WrongArgEx('permissions', structure.get('permissions'))

    if 'features' not in structure or \
            not isinstance(structure['features'], list):
        raise ex.WrongArgEx('features', structure.get('features'))

    feats = structure['features']
    perms = structure['permissions']

    tool_id = _get_int_id_or_err(tool_id, 'tool_id')
    tool = wha.get_tool_by_id(sess, tool_id)
    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)

    # Create & validate features to add
    features_to_add = []
    for _f in feats:
        features_to_add.append({
            'name': _f.get('name')
        })

    # Create & validate permissions to add
    _perms = {
        'ent_type': {},
        'var_type': {},
        'ts_type': {},
        'tp_type': {}
    }
    for _p in perms:
        if _p['node_type'] == 'ent':
            type = 'ent_type'
        elif _p['node_type'] == 'var':
            type = 'var_type'
        elif _p['node_type'] == 'ts':
            type = 'ts_type'
        elif _p['node_type'] == 'tp':
            type = 'tp_type'

        _perms[type][_p['node_id']] = _p

    # _perms[node_type][node_id] = {}
    for node_id, v in _perms['tp_type'].items():
        if not v or not v['parent_node_id'] \
                or not _perms['ts_type'].get(v['parent_node_id']):
            raise ex.WrongArgsError('insert_permissions()')

    for node_id, v in _perms['ts_type'].items():
        if not v or not v['parent_node_id'] \
                or not _perms['var_type'].get(v['parent_node_id']):
            raise ex.WrongArgsError('insert_permissions()')

    for node_id, v in _perms['var_type'].items():
        if not v or not v['parent_node_id'] \
                or not _perms['ent_type'].get(v['parent_node_id']):
            raise ex.WrongArgsError('insert_permissions()')

    # Add features
    if len(features_to_add) > 0:
        for f in features_to_add:
            wha.add_feature(sess, f['name'], tool)


    # Add permissions
    for node_id, value in _perms['ent_type'].items():
        real = wha.add_perm_node(sess, tool, 'ent')
        if real is not None:
            wha.add_default_perm_value(sess, tool, real, v['mask'])
            _perms['ent_type'][node_id]['real'] = real
        else:
            raise ex.CreatingError('PermNode')

    for node_id, value in _perms['var_type'].items():
        parent = _perms['ent_type'][value['parent_node_id']]['real']
        real = wha.add_perm_node(sess, tool, 'var', parent)
        if real is not None:
            wha.add_default_perm_value(sess, tool, real, v['mask'])
            _perms['var_type'][node_id]['real'] = real
        else:
            raise ex.CreatingError('PermNode')

    for node_id, value in _perms['ts_type'].items():
        parent = _perms['var_type'][value['parent_node_id']]['real']
        real = wha.add_perm_node(sess, tool, 'ts', parent)
        if real is not None:
            wha.add_default_perm_value(sess, tool, real, v['mask'])
            _perms['ts_type'][node_id]['real'] = real
        else:
            raise ex.CreatingError('PermNode')

    for node_id, value in _perms['tp_type'].items():
        parent = _perms['ts_type'][value['parent_node_id']]['real']
        real = wha.add_perm_node(sess, tool, 'tp', parent)
        if real is not None:
            wha.add_default_perm_value(sess, tool, real, v['mask'])
            _perms['tp_type'][node_id]['real'] = real
        else:
            raise ex.CreatingError('PermNode')
