from .. import exceptions as ex
from ..db import layer_access as wha
from .service import (
    get_int_id_or_err as _get_id_or_err,
    get_str_or_err as _get_str_or_err
)


class IManageAccess:
    def __init__(self):
        pass

    def set_permissions_template(self, ssn, tool_id, template):
        if 'permissions' not in template or \
                not isinstance(template['permissions'], list):
            raise ex.WrongArgEx('permissions', template.get('permissions'))

        if 'features' not in template or \
                not isinstance(template['features'], list):
            raise ex.WrongArgEx('features', template.get('features'))

        feats = template['features']
        perms = template['permissions']

        tool_id = _get_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        # Create & validate features to add
        features_to_add = []
        for _f in feats:
            features_to_add.append({
                'name': _f.get('name')
            })

        # Add permissions
        perms = sorted(perms, key=lambda perm: len(perm['path']))
        store = {}
        for _perm in perms:
            n_type = _perm['node_type']
            n_name = _perm['name']
            n_path = _perm['path']

            tl = ['ent' for x in _perm['path']]
            last = len(tl) - 1
            if n_type == 'tp':
                tl[last] = 'ts'
                tl[last - 1] = 'var'
                tl[last - 2] = 'ent'
            elif n_type == 'ts':
                tl[last] = 'var'
                tl[last - 1] = 'ent'
            elif n_type == 'var':
                tl[last] = 'ent'
            elif n_type == 'ent':
                pass

            par_path_str = ".".join(n_path)
            n_path_str = par_path_str + '.' + n_name
            store[n_path_str] = wha.add_perm_node(ssn, tool, n_type, n_name)
            wha.add_default_perm_value(ssn, tool, store[n_path_str],
                                       _perm['mask'])

            if store.get(par_path_str) is None:
                par_key = None
                for i, node_name in enumerate(n_path):
                    node_type = tl[i]
                    node_path = node_name if par_key is None \
                        else par_key + '.' + node_name
                    store[node_path] = wha.add_perm_node(ssn, tool, node_type,
                                                         node_name)
                    if par_key is not None:
                        store[par_key].children.append(store[node_path])
                    par_key = node_path

                par_path_str = par_key

            store[par_path_str].children.append(store[n_path_str])

        # Add features
        if len(features_to_add) > 0:
            for f in features_to_add:
                wha.add_feature(ssn, f['name'], tool)

    def init_user_wb(self, user_id, tool_id):
        pass  # TODO Realize

    def add_user(self, ssn, email, password, roles_id=None):
        email = _get_str_or_err(email, 'email')
        password = _get_str_or_err(password, 'password')  # TODO Hashing Pass
        roles = []
        if roles_id is not None and isinstance(roles_id, list):
            for role_id in roles_id:
                role_id = _get_id_or_err(role_id, 'id')
                role = wha.get_role_by_id(ssn, role_id)
                if role is None:
                    raise ex.NotExistsError('Role', 'id', role_id)
                else:
                    roles.append(role)

        existed = wha.get_user_by_email(ssn, email)
        if existed is not None:
            raise ex.AlreadyExistsError('User', 'email', email)

        return wha.add_user(ssn, email, password, roles)

    def add_role(self, ssn, name, tool_id):
        name = _get_str_or_err(name, 'name')

        tool_id = _get_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        existed = [role for role in tool.roles if role.name == name]
        if existed is not None or len(existed):
            raise ex.AlreadyExistsError('Role', 'name', name)

        new_role = wha.add_role(ssn, name)
        # wha.add_role_to_tool(ssn, new_role, tool)
        tool.roles.append(new_role)
        return new_role

    def get_users(self, ssn, tool_id=None):
        if tool_id is not None:
            tool_id = _get_id_or_err(tool_id, 'tool_id')
            tool = wha.get_tool_by_id(ssn, tool_id)
            if tool is None:
                raise ex.NotExistsError('Tool', 'id', tool_id)

            return wha.get_users_by_tool(ssn, tool)

        return wha.get_all_users(ssn)

    def get_roles(self, ssn, tool_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        return tool.roles

    def get_features(self, ssn, tool_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        return wha.get_features_by_tool(ssn, tool)

    def get_role_features(self, ssn, role_id):
        role_id = _get_id_or_err(role_id, 'id')

        role = wha.get_role_by_id(ssn, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)

        return role.features

    def update_role_features(self, ssn, role_id, features_id):
        role_id = _get_id_or_err(role_id, 'id')

        role = wha.get_role_by_id(ssn, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)

        if features_id is None or not isinstance(features_id, list):
            raise ex.WrongArgEx('features_id', features_id)

        new_features = []
        for fid in features_id:
            f = wha.get_feature_by_id(fid)
            if f is not None:
                new_features.append(f)
            else:
                raise ex.NotExistsError('Feature', 'id', fid)

        old_f = [x.id for x in role.features]
        new_f = features_id

        to_keep = set(old_f).intersection(new_f)
        # Delete
        if len(old_f) > len(to_keep):
            delete_ids = set(old_f) - set(to_keep)
            wha.del_features_from_role(ssn, role, delete_ids)
        # Add
        if len(new_f) > len(to_keep):
            add = set(new_f) - set(to_keep)
            to_add_features = [x for x in new_features if x.id in add]
            wha.add_features_to_role(ssn, role, to_add_features)

        return role.features

    def add_group(self, ssn, name, tool_id):
        name = _get_str_or_err(name, 'name')
        tool_id = _get_id_or_err(tool_id, 'tool_id')

        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        existing = [ug for ug in tool.user_groups if ug.name == name]
        #  TODO Check
        if existing is not None and isinstance(existing, list):
            raise ex.AlreadyExistsError('UserGroup', 'name', name)

        return wha.add_user_group(ssn, name, tool)

    def get_group_users(self, ssn, group_id):
        group_id = _get_id_or_err(group_id, 'group_id')

        group = wha.get_user_group_by_id(ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        return group.users

    def get_group_data_perimissions(self, ssn, group_id, tool_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        group_id = _get_id_or_err(group_id, 'group_id')

        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        group = wha.get_user_group_by_id(ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        pass  # TODO Realize

    def add_user_to_group(self, ssn, user_id, group_id):
        user_id = _get_id_or_err(user_id, 'user_id')
        group_id = _get_id_or_err(group_id, 'group_id')

        user = wha.get_user_by_id(ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        group = wha.get_user_group_by_id(ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        if user in group.users:
            raise ex.AlreadyExistsError('UserGroup', 'users', user.id)

        return group.users.append(user)

    def add_data_permissions_to_group(self):
        pass  # TODO Realize

    def update_group_data_permissions(self):
        pass  # TODO Realize

    def update_user_data_permissions(self):
        pass  # TODO Realize

    ###########################

    def get_role(self, ssn, **kwargs):
        """
        Args:
            ssn
            **kwargs: id|name
        """
        if 'id' in kwargs:
            role_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_role_by_id(ssn, role_id)

        elif 'name' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            return wha.get_role_by_name(ssn, name)

    def get_user(self, ssn, **kwargs):
        """
        Args:
            ssn
            **kwargs: id|email
        """
        if 'id' in kwargs:
            user_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_user_by_id(ssn, user_id)

        elif 'email' in kwargs:
            email = _get_str_or_err(kwargs['email'], 'email')
            return wha.get_user_by_email(ssn, email)

    def get_tool(self, ssn, **kwargs):
        """
        Args:
            ssn
            **kwargs: id|email
        """
        if 'id' in kwargs:
            tool_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_tool_by_id(ssn, tool_id)

        elif 'name' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            return wha.get_tool_by_name(ssn, name)

    def get_feature(self, ssn, **kwargs):
        """
        Args:
            ssn
            **kwargs: id|name & tool_id
        """
        if 'id' in kwargs:
            feature_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_feature_by_id(ssn, feature_id)

        elif 'name' in kwargs and 'tool_id' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            tool_id = _get_id_or_err(kwargs['tool_id'], 'tool_id')
            tool = wha.get_tool_by_id(ssn, tool_id)
            if tool is None:
                raise ex.NotExistsError('Tool', 'id', tool_id)
            return wha.get_feature_by_name_in_tool(ssn, name, tool)

    # def add_role_to_tool(self, ssn, role_id, tool_id):
    #     role_id = _get_id_or_err(role_id, 'id')
    #     tool_id = _get_id_or_err(tool_id, 'tool_id')
    #
    #     role = wha.get_role_by_id(ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     tool = wha.get_tool_by_id(ssn, tool_id)
    #     if tool is None:
    #         raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #     # TODO Check Existed
    #     return wha.add_role_to_tool(ssn, role, tool)

    # def add_role_to_user(self, ssn, user_id, role_id):
    #     user_id = _get_id_or_err(user_id, 'id')
    #     role_id = _get_id_or_err(role_id, 'id')
    #
    #     role = wha.get_role_by_id(ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     user = wha.get_user_by_id(ssn, user_id)
    #     if user is None:
    #         raise ex.NotExistsError('User', 'id', user_id)
    #
    #     return wha.add_role_to_user(ssn, user, role)

    # def add_tool(self, ssn, name):
    #     name = _get_str_or_err(name, 'name')
    #     existed = wha.get_tool_by_name(ssn, name)
    #     if existed is not None:
    #         raise ex.AlreadyExistsError('Tool', 'name', name)
    #     return wha.add_tool(ssn, name)

    # def add_feature(self, ssn, name, tool_id=None, role_id=None):
    #     name = _get_str_or_err(name, 'name')
    #     tool = None
    #     if tool_id is not None:
    #         tool_id = _get_id_or_err(tool_id, 'tool_id')
    #         tool = wha.get_tool_by_id(ssn, tool_id)
    #         if tool is None:
    #             raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #         existed = wha.get_feature_by_name_in_tool(ssn, name, tool)
    #         if existed is not None:
    #             raise ex.AlreadyExistsError('Feature', 'name', name)
    #
    #     role = None
    #     if role_id is not None:
    #         role_id = _get_id_or_err(role_id, 'role_id')
    #         role = wha.get_role_by_id(ssn, role_id)
    #         if role is None:
    #             raise ex.NotExistsError('Role', 'id', role_id)
    #
    #         existed = wha.get_feature_by_name_in_role(ssn, name, role)
    #         if existed is not None:
    #             raise ex.AlreadyExistsError('Feature', 'name', name)
    #
    #     return wha.add_feature(ssn, name, tool, role)

    # def add_feature_to_tool(self, ssn, feature_id, tool_id):
    #     tool_id = _get_id_or_err(tool_id, 'tool_id')
    #     feature_id = _get_id_or_err(feature_id, 'feature_id')
    #
    #     feature = wha.get_feature_by_id(ssn, feature_id)
    #     if feature is None:
    #         raise ex.NotExistsError('Feature', 'id', feature_id)
    #
    #     tool = wha.get_tool_by_id(ssn, tool_id)
    #     if tool is None:
    #         raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #     return wha.add_feature_to_tool(ssn, feature, tool)

    # def add_feature_to_role(self, ssn, feature_id, role_id):
    #     role_id = _get_id_or_err(role_id, 'tool_id')
    #     feature_id = _get_id_or_err(feature_id, 'feature_id')
    #
    #     feature = wha.get_feature_by_id(ssn, feature_id)
    #     if feature is None:
    #         raise ex.NotExistsError('Feature', 'id', feature_id)
    #
    #     role = wha.get_role_by_id(ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     return wha.add_feature_to_role(ssn, role, feature)

    def add_permission(self, ssn, tool_id, node_type, name, parent_id=None):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        node_type = _get_str_or_err(node_type, 'node_type')  # Defined string
        name = _get_str_or_err(name, 'name')

        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        parent = None
        if parent_id is not None:
            parent_id = _get_id_or_err(parent_id, 'parent_id')
            parent = wha.get_perm_node_in_tool(ssn, parent_id, tool)
            if parent is None:
                raise ex.NotExistsError('PermNode', 'id', parent_id)

        return wha.add_perm_node(ssn, tool, node_type, name, parent)

    def add_permission_value(self, ssn, tool_id, perm_node_id, value, user_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        perm_node_id = _get_id_or_err(perm_node_id, 'perm_node_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        tool = wha.get_tool_by_id(ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        user = wha.get_user_by_id(ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        perm_node = wha.get_perm_node_in_tool(ssn, perm_node_id, tool)
        if perm_node is None:
            raise ex.NotExistsError('PermNode', 'id', perm_node_id)

        return wha.add_perm_value(ssn, tool, perm_node, value, user)
