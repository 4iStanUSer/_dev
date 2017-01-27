import copy

from iap.common.repository.models_managers import layer_access as wha
from iap.common.repository.models_managers.iaccess import IAccess as _IAccess
from iap.common.repository.interface.service import (
    get_int_id_or_err as _get_id_or_err,
    get_str_or_err as _get_str_or_err
)
from iap.common.repository import exceptions as ex


class IManageAccess:

    def __init__(self, **kwargs):
        try:
            self.ssn = kwargs['ssn'] if kwargs.get('ssn') is not None \
                else kwargs['ssn_factory']()
        except KeyError:
            raise Exception  # TODO update

    def set_permissions_template(self, tool_id, template):
        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        if 'permissions' not in template or \
                not isinstance(template['permissions'], list):
            raise ex.WrongArgEx('permissions', template.get('permissions'))

        if 'features' not in template or \
                not isinstance(template['features'], list):
            raise ex.WrongArgEx('features', template.get('features'))

        feats = template['features']
        perms = template['permissions']



        # Get objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        # Create & validate features dict for adding
        features_to_add = []
        for _f in feats:
            features_to_add.append({
                'name': _f.get('name')
            })

        # Add permissions
        perms = sorted(perms, key=lambda perm: len(perm['path']))
        storage = {}
        for perm in perms:
            self._add_permission(tool, storage, perm)

        # Add default features for tool
        if len(features_to_add) > 0:
            for f in features_to_add:
                wha.add_feature(self.ssn, f['name'], tool)

        return None

    def init_user_wb(self, user_id, tool_id):
        #???
        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        # Get Objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)
        user = wha.get_user_by_id(self.ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        # Version 2
        # Get raw data from table with masks
        raw_perm_values = wha.get_raw_perm_values_for_user(self.ssn, tool, None)

        # Copy/Insert this raw data for specified user
        # TODO - check if there is no data for this user!!!
        for per_v in raw_perm_values:
            perm_node = per_v.perm_node
            wha.add_perm_value(self.ssn, tool, perm_node, per_v.value, user)

        # TODO Fix bug with initialize db
        # # Get recently created permissions for user
        iaccess = _IAccess(ssn=self.ssn)
        u_perms = iaccess.get_permissions(tool_id, user_id)

        # self.istorage.backup.save(user_id, tool_id, u_perms, 'models_managers')

        # # Make backup file
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # file_name = "backup_tool_" + str(tool_id) + "_user_" \
        #             + str(user_id) + ".json"
        # file_path = os.path.join(dir_path, file_name)
        # with open(file_path, "w+") as backup_file:
        #     json.dump(u_perms, backup_file)

        pass  # TODO Confirm This Realization

    def add_user(self, email, password, roles_id=None):
        # Validate inputs
        email = _get_str_or_err(email, 'email')
        password = _get_str_or_err(password, 'password')  # TODO Hashing Pass

        # Get Objects
        roles = []
        if roles_id is not None and isinstance(roles_id, list):
            for role_id in roles_id:
                role_id = _get_id_or_err(role_id, 'id')
                role = wha.get_role_by_id(self.ssn, role_id)
                if role is None:
                    raise ex.NotExistsError('Role', 'id', role_id)
                else:
                    roles.append(role)

        existing = wha.get_user_by_email(self.ssn, email)
        if existing is not None:
            raise ex.AlreadyExistsError('User', 'email', email)

        return wha.add_user(self.ssn, email, password, roles)

    def add_role(self, name, tool_id):
        """
        Add role is correct
        :param name:
        :type name:
        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs
        name = _get_str_or_err(name, 'name')
        tool_id = _get_id_or_err(tool_id, 'tool_id')

        # Get Objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        existing = [role for role in tool.roles if role.name == name]
        if existing is not None and len(existing) > 0:
            raise ex.AlreadyExistsError('Role', 'name', name)

        new_role = wha.add_role(self.ssn, name)
        # wha.add_role_to_tool(self.ssn, new_role, tool)
        tool.roles.append(new_role)
        return new_role

    def get_users(self, tool_id=None):
        """
        Return user object by given tool

        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs & Get object
        if tool_id is not None:
            tool_id = _get_id_or_err(tool_id, 'tool_id')
            tool = wha.get_tool_by_id(self.ssn, tool_id)
            if tool is None:
                raise ex.NotExistsError('Tool', 'id', tool_id)

            return wha.get_users_by_tool(self.ssn, tool)

        return wha.get_all_users(self.ssn)

    def get_user_roles(self, user_id):
        """
        Return Users Role's

        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """
        user_id = _get_id_or_err(user_id, 'user_id')
        user = wha.get_user_by_id(self.ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        return user.roles

    def get_roles(self, tool_id):
        """
        Return roles related to given tool

        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'tool_id')

        # Get Objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        return tool.roles

    def get_features(self, tool_id):
        """
        Return features related to given tool

        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'tool_id')

        # Get Objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        return wha.get_features_by_tool(self.ssn, tool)

    def get_role_features(self, role_id):
        """
        Return Features related to Role

        :param role_id:
        :type role_id:
        :return:
        :rtype:
        """
        # Validate inputs
        role_id = _get_id_or_err(role_id, 'id')

        # Get Objects
        role = wha.get_role_by_id(self.ssn, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)

        return role.features

    def update_role_features(self, role_id, features_id):
        """
        Update role by given list of features.
        Delete non common features, and add new

        :param role_id:
        :type role_id:
        :param features_id:
        :type features_id:
        :return:
        :rtype:
        """
        # Validate inputs
        role_id = _get_id_or_err(role_id, 'id')
        if features_id is None or not isinstance(features_id, list):
            raise ex.WrongArgEx('features_id', features_id)

        # Get Objects
        role = wha.get_role_by_id(self.ssn, role_id)
        if role is None:
            raise ex.NotExistsError('Role', 'id', role_id)
        new_features = []
        for fid in features_id:
            f = wha.get_feature_by_id(self.ssn, fid)
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
            wha.del_features_from_role(self.ssn, role, delete_ids)
        # Add
        if len(new_f) > len(to_keep):
            add = set(new_f) - set(to_keep)
            to_add_features = [x for x in new_features if x.id in add]
            wha.add_features_to_role(self.ssn, role, to_add_features)

        return role.features

    def add_group(self, name, tool_id):
        """
        Add user group to Tool

        :param name:
        :type name:
        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs
        name = _get_str_or_err(name, 'name')
        tool_id = _get_id_or_err(tool_id, 'tool_id')

        # Get Objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        existing = [ug for ug in tool.user_groups if ug.name == name]
        #  TODO Check
        if existing is not None and isinstance(existing, list):
            raise ex.AlreadyExistsError('UserGroup', 'name', name)

        return wha.add_user_group(self.ssn, name, tool)

    def get_group_users(self, group_id):
        """

        Return Get User of Specific Group

        :param group_id:
        :type group_id:
        :return:
        :rtype:
        """
        # Validate inputs
        group_id = _get_id_or_err(group_id, 'group_id')

        # Get objects
        group = wha.get_user_group_by_id(self.ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        return group.users

    def check_permission_for_tool_and_project(self, user_id, tool_id, project_id):
        """
        Function will check permission to project and tool


        :return:
        :rtype:

        """
        access = {'tool':False, 'project':False}
        user = wha.get_user_by_id(self.ssn, user_id)
        for role in user.roles:
            if tool_id == role.tool_id:
                access['tool': True]
        for perm in user.perms:
            for data_perm in perm:
                if data_perm.project == project_id:
                    access['project': True]
        if access == {'tool':True, 'project':True}:
            return True
        else:
            return False

    def get_entity_permission(self, user_id, project_id, entity_path):
        """

        :param user_id:
        :type user_id:
        :param project_id:
        :type project_id:
        :param entity_path:
        :type entity_path:
        :return:
        :rtype:
        """
        user = wha.get_user_by_id(user_id)
        perms = user.perms
        for perm in perms:
            pass
        
    def get_group_data_permissions(self, group_id, tool_id):
        """
        TEMPRORARY DOESN'T WORK

        TO DO Method don't return anything
        Ver.1 - Get data by group
        Q:Why to put tool_id if data models_managers is fully defined by group_id?

        :param group_id:
        :type group_id:
        :param tool_id:
        :type tool_id:
        :return:
        :rtype:
        """
        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        group_id = _get_id_or_err(group_id, 'group_id')

        # Get objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        group = wha.get_user_group_by_id(self.ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        return wha.get_data_permission(group_id)

    def add_user_to_group(self, user_id, group_id):
        """
        TEMPRORARY DOESN'T WORK

        Add user to group

        :param user_id:
        :type user_id:
        :param group_id:
        :type group_id:
        :return:
        :rtype:
        """
        # Validate inputs
        user_id = _get_id_or_err(user_id, 'user_id')
        group_id = _get_id_or_err(group_id, 'group_id')

        # Get objects
        user = wha.get_user_by_id(self.ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)
        group = wha.get_user_group_by_id(self.ssn, group_id)
        if group is None:
            raise ex.NotExistsError('UserGroup', 'id', group_id)

        if user in group.users:
            raise ex.AlreadyExistsError('UserGroup', 'users', user.id)

        return group.users.append(user)

    def add_data_permissions_to_group(self, group_id, permisssions_id):
        """
        TEMPRORARY DOESN'T WORK

        :param group_id:
        :type group_id:
        :param permisssions_id:
        :type permisssions_id:
        :return:
        :rtype:
        """
        group_id = _get_id_or_err(group_id, 'group_id')
        group = wha.get_user_group_by_id(self.ssn, group_id)
        permissions = []
        for perm_id in permisssions_id:
            if perm_id in [perm.id for perm in group.data_perm]:
                pass
            else:
                perm_data_access = wha.get_data_permission_by_id(perm_id)
                permissions.append(perm_data_access)
                group.data_perm.append(perm_data_access)
        return permissions

    def update_group_data_permissions(self, group_id, permisssions_id):
        """
        TEMPRORARY DOESN'T WORK
        :param group_id:
        :type group_id:
        :param permisssions_id:
        :type permisssions_id:
        :return:
        :rtype:
        """
        group_id = _get_id_or_err(group_id, 'group_id')
        group = wha.get_user_group_by_id(self.ssn, group_id)
        group_data_perm = [data_perm.id for data_perm in group.data_perm]

        to_keep = set(group_data_perm).intersection(permisssions_id)
        # Delete
        if len(group_data_perm) > len(permisssions_id):
            delete_ids = set(group_data_perm) - set(to_keep)
            wha.del_perm_data_from_group(self.ssn, group_id, delete_ids)
            #TO DO del_perm_data_from_group
        # Add
        if len(group_data_perm) > len(to_keep):
            add = set(permisssions_id) - set(to_keep)
            to_add_features = [x for x in permisssions_id if x.id in add]
            wha.add_perm_data_from_group(self.ssn, group_id, to_add_features)
            #TO DO add_perm_data_from_group
        return to_keep

    def update_user_data_permissions(self, tool_id, user_id, permissions):
        """
        TEMPRORARY DOESN'T WORK
        :param tool_id:
        :type tool_id:
        :param user_id:
        :type user_id:
        :param permissions:
        :type permissions:
        :return:
        :rtype:
        """
        #TODO

        # Validate inputs
        tool_id = _get_id_or_err(tool_id, 'user_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        # Get objects
        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)
        user = wha.get_user_by_id(self.ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        # TODO Validating paths for nodes

        # Delete previous permissions for user
        wha.del_perm_values_for_user(self.ssn, tool, user)

        # Get objects
        storage = {}
        permissions = sorted(permissions, key=lambda p: len(p['path']))
        for perm in permissions:
            self._add_permission(tool, storage, perm, user)

    def _add_permission(self, tool, storage, perm, user=None):
        """
        TEMPRORARY DOESN'T WORK

        Adds permission node(PermNode obj) into variable 'storage'.
        Looks for existing parent and adds into him as child node.
        Inserts all not existing parents.
        :param tool: Tool obj
        :param storage: dictionary for store nodes for future adding
        :param perm: dictionary, keys: node_type, name, path, mask
        :param user: User obj
        :return: created PermNode obj
        """
        n_type = perm.get('node_type')
        n_name = perm.get('name')
        n_path = perm['path'] if perm.get('path') is not None else []
        n_mask = perm.get('mask')

        n_path_storage = copy.deepcopy(n_path)
        n_path_storage.append(n_name)
        n_path_storage = tuple(n_path_storage)
        n_path_tpl = tuple(n_path)

        # Generate list of types for path
        tl = self._get_node_types_from_path(n_path, n_type)

        # Create Node
        if n_path_storage not in storage:
            node = self._get_permission_node(tool, n_path,
                                             n_name)
            if node is None:
                storage[n_path_storage] = wha.add_perm_node(self.ssn, tool, n_type,
                                                            n_name)
            else:
                storage[n_path_storage] = node

        # Create Value(mask) & connect with created Node (if mask exists)
        if n_mask is not None:
            if user is None:
                wha.add_default_perm_value(self.ssn, tool, storage[n_path_storage],
                                           n_mask)
            else:
                wha.add_perm_value(self.ssn, tool, storage[n_path_storage], n_mask,
                                   user)

        # Get Node's parent & inject node into parent's children
        if len(n_path) > 0:
            if n_path_tpl not in storage:
                # Define parent's data
                par_n_name = n_path[-1]
                par_n_type = tl[-1]
                par_n_path = []
                if len(n_path) > 1:
                    par_n_path = n_path[:-1]

                # Get from DB
                par_perm = {
                    'node_type': par_n_type,
                    'name': par_n_name,
                    'path': par_n_path
                }
                par_node = self._get_permission_node(tool, par_n_path,
                                                     par_n_name)
                if par_node is not None:
                    storage[n_path_tpl] = par_node
                else:
                    storage[n_path_tpl] = self._add_permission(tool,
                                                               storage,
                                                               par_perm)

            storage[n_path_tpl].children.append(storage[n_path_storage])

        return storage[n_path_storage]

    def _get_permission_node(self, tool, path, name):
        """
        TEMPRORARY DOESN'T WORK

        Look for permission node in DB for tool by name and path
        :param tool: Tool instance
        :param path: list strings(parents' names)
        :param name: string - name of node
        :return: PermNode object | None
        """
        nodes = wha.get_nodes_by_name(self.ssn, tool, name)
        if len(nodes) == 0:
            return None

        chains = {}
        nodes_d = {}
        for node in nodes:
            chains[node.id] = []
            nodes_d[node.id] = node

        rev_path = path[::-1]

        for node in nodes:

            n = node
            for inx, par_name in enumerate(rev_path):
                found = False
                if n is not None and len(n.parents) > 0:
                    for parent in n.parents:
                        if par_name == parent.name:
                            found = True
                            chains[node.id].append(parent)
                            n = parent
                            break
                if not found:
                    # Exclude node_id from chains
                    chains.pop(node.id, None)
                    break

        if len(chains) == 0:
            return None
        elif len(chains) == 1:
            return nodes_d[next(iter(chains.keys()))]
        else:
            pass  # TODO NotCorrectDataError

    def _get_node_types_from_path(self, path, n_type):
        """
        TEMPRORARY DOESN'T WORK

        Generate list of types for path of this node.
        Output list has same length as variable 'path'.
        Example:
            Input:
                path - ['Argentina', 'Chocolate', 'Praline', 'Unit', 'Annual']
                n_type - 'tp'
            Output:
                ['ent', 'ent', 'ent', 'var', 'ts']
        :param path: list of strings(path)
        :param n_type: string(ent|var|ts|tp)
        :return: list with parents' type
        """
        tl = ['ent' for x in path]
        last_ind = len(tl) - 1
        if n_type == 'tp':
            tl[last_ind] = 'ts'
            if len(tl) > 1:
                tl[last_ind - 1] = 'var'
            if len(tl) > 2:
                tl[last_ind - 2] = 'ent'
        elif n_type == 'ts':
            tl[last_ind] = 'var'
            if len(tl) > 1:
                tl[last_ind - 1] = 'ent'
        elif n_type == 'var':
            tl[last_ind] = 'ent'
        elif n_type == 'ent':
            pass

        return tl

    ###########################

    def get_role(self, **kwargs):
        """
        Args:
            **kwargs: id|name
        """
        if 'id' in kwargs:
            role_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_role_by_id(self.ssn, role_id)

        elif 'name' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            return wha.get_role_by_name(self.ssn, name)

    def get_user(self, **kwargs):
        """
        Args:
            **kwargs: id|email
        """
        if 'id' in kwargs:
            user_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_user_by_id(self.ssn, user_id)

        elif 'email' in kwargs:
            email = _get_str_or_err(kwargs['email'], 'email')
            return wha.get_user_by_email(self.ssn, email)

    def get_tool(self, **kwargs):
        """
        Args:
            **kwargs: id|email
        """
        if 'id' in kwargs:
            tool_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_tool_by_id(self.ssn, tool_id)

        elif 'name' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            return wha.get_tool_by_name(self.ssn, name)

    def get_feature(self, **kwargs):
        """
        Args:
            **kwargs: id|name & tool_id
        """
        if 'id' in kwargs:
            feature_id = _get_id_or_err(kwargs['id'], 'id')
            return wha.get_feature_by_id(self.ssn, feature_id)

        elif 'name' in kwargs and 'tool_id' in kwargs:
            name = _get_str_or_err(kwargs['name'], 'name')
            tool_id = _get_id_or_err(kwargs['tool_id'], 'tool_id')
            tool = wha.get_tool_by_id(self.ssn, tool_id)
            if tool is None:
                raise ex.NotExistsError('Tool', 'id', tool_id)
            return wha.get_feature_by_name_in_tool(self.ssn, name, tool)

    # def add_role_to_tool(self, role_id, tool_id):
    #     role_id = _get_id_or_err(role_id, 'id')
    #     tool_id = _get_id_or_err(tool_id, 'tool_id')
    #
    #     role = wha.get_role_by_id(self.ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     tool = wha.get_tool_by_id(self.ssn, tool_id)
    #     if tool is None:
    #         raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #     # TODO Check Existed
    #     return wha.add_role_to_tool(self.ssn, role, tool)

    # def add_role_to_user(self, user_id, role_id):
    #     user_id = _get_id_or_err(user_id, 'id')
    #     role_id = _get_id_or_err(role_id, 'id')
    #
    #     role = wha.get_role_by_id(self.ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     user = wha.get_user_by_id(self.ssn, user_id)
    #     if user is None:
    #         raise ex.NotExistsError('User', 'id', user_id)
    #
    #     return wha.add_role_to_user(self.ssn, user, role)

    def add_tool(self, name):
        name = _get_str_or_err(name, 'name')
        existing = wha.get_tool_by_name(self.ssn, name)
        if existing is not None:
            raise ex.AlreadyExistsError('Tool', 'name', name)
        return wha.add_tool(self.ssn, name)

    # def add_feature(self, name, tool_id=None, role_id=None):
    #     name = _get_str_or_err(name, 'name')
    #     tool = None
    #     if tool_id is not None:
    #         tool_id = _get_id_or_err(tool_id, 'tool_id')
    #         tool = wha.get_tool_by_id(self.ssn, tool_id)
    #         if tool is None:
    #             raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #         existing = wha.get_feature_by_name_in_tool(self.ssn, name, tool)
    #         if existing is not None:
    #             raise ex.AlreadyExistsError('Feature', 'name', name)
    #
    #     role = None
    #     if role_id is not None:
    #         role_id = _get_id_or_err(role_id, 'role_id')
    #         role = wha.get_role_by_id(self.ssn, role_id)
    #         if role is None:
    #             raise ex.NotExistsError('Role', 'id', role_id)
    #
    #         existing = wha.get_feature_by_name_in_role(self.ssn, name, role)
    #         if existing is not None:
    #             raise ex.AlreadyExistsError('Feature', 'name', name)
    #
    #     return wha.add_feature(self.ssn, name, tool, role)

    # def add_feature_to_tool(self, feature_id, tool_id):
    #     tool_id = _get_id_or_err(tool_id, 'tool_id')
    #     feature_id = _get_id_or_err(feature_id, 'feature_id')
    #
    #     feature = wha.get_feature_by_id(self.ssn, feature_id)
    #     if feature is None:
    #         raise ex.NotExistsError('Feature', 'id', feature_id)
    #
    #     tool = wha.get_tool_by_id(self.ssn, tool_id)
    #     if tool is None:
    #         raise ex.NotExistsError('Tool', 'id', tool_id)
    #
    #     return wha.add_feature_to_tool(self.ssn, feature, tool)

    # def add_feature_to_role(self, feature_id, role_id):
    #     role_id = _get_id_or_err(role_id, 'tool_id')
    #     feature_id = _get_id_or_err(feature_id, 'feature_id')
    #
    #     feature = wha.get_feature_by_id(self.ssn, feature_id)
    #     if feature is None:
    #         raise ex.NotExistsError('Feature', 'id', feature_id)
    #
    #     role = wha.get_role_by_id(self.ssn, role_id)
    #     if role is None:
    #         raise ex.NotExistsError('Role', 'id', role_id)
    #
    #     return wha.add_feature_to_role(self.ssn, role, feature)

    def add_permission(self, tool_id, node_type, name, parent_id=None):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        node_type = _get_str_or_err(node_type, 'node_type')  # Defined string
        name = _get_str_or_err(name, 'name')

        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        parent = None
        if parent_id is not None:
            parent_id = _get_id_or_err(parent_id, 'parent_id')
            parent = wha.get_perm_node_in_tool(self.ssn, parent_id, tool)
            if parent is None:
                raise ex.NotExistsError('PermNode', 'id', parent_id)

        return wha.add_perm_node(self.ssn, tool, node_type, name, parent)

    def add_permission_value(self, tool_id, perm_node_id, value, user_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        perm_node_id = _get_id_or_err(perm_node_id, 'perm_node_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        tool = wha.get_tool_by_id(self.ssn, tool_id)
        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)

        user = wha.get_user_by_id(self.ssn, user_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        perm_node = wha.get_perm_node_in_tool(self.ssn, perm_node_id, tool)
        if perm_node is None:
            raise ex.NotExistsError('PermNode', 'id', perm_node_id)

        return wha.add_perm_value(self.ssn, tool, perm_node, value, user)