

from . models import *


class WarehouseAccess():
    '''
    Class for user roles management. 
    '''
    def __init__(self, db_connector, warh_common):
        self.db = db_connector
        self.warh_common = warh_common

    #region Role permissions
    def add_perms_to_role(self, role, permissions):
        if role is None:
            raise ex.EmptyInputsError('role')
        role.feature_permissions.extend(permissions)
        self.db.session.commit()
        return role

    def get_role_perms(self, role):
        if role is None:
            raise ex.EmptyInputsError('role')
        return role.feature_permissions

    def delete_role_perms(self, role, permissions):
        '''Attributes
        role - object
        permissions - id
        '''
        if role is None:
            raise ex.EmptyInputsError('role')
        if len(permissions) == 0:
            raise ex.WrongArgsError('delete_role_perms')
        if len(role.feature_permissions) == 0:
            raise ex.NotExistsError('Role.feature_permissions',
                                    'feature_permissions',
                                    'feature_permissions')
        need_commit = False
        for id in permissions:
            del_index = -1
            for i in len(role.feature_permissions):
                if role.feature_permissions[i].id == id:
                    del_index = i
                    need_commit = True
            if del_index >= 0:
                del role.feature_permissions[del_index]
            else:
                raise ex.NotExistsError('FeaturePermission', 'id', id)
        if need_commit:
            self.db.session.commit()
        else:
            raise ex.NoCnahgesError('FeaturePermission', 'delete_role_perms')

    def update_role_perms(self, role, permissions):
        '''Attributes
        role - object
        permissions - feature_permissions_ids
        '''
        need_commit = False
        if role is None:
            raise ex.EmptyInputsError('role')
        if not isinstance(permissions, list):
            raise ex.EmptyInputsError('FeaturePermission')
        if len(permissions) == 0:
            raise ex.EmptyInputsError('FeaturePermission')
        #delete
        ids_to_del = []
        for perm in role.feature_permissions:
            is_matched = False
            for item_id in permissions:
                if perm.id == item_id:
                    is_matched = True
                    break
            if not is_matched:
                ids_to_del.append(perm.id)
        #add
        to_add_ids = []
        for new_id in permissions:
            is_not_found = True
            for perm in role.feature_permissions:
                if perm.id == new_id:
                    is_not_found = False
                    break
            if is_not_found:
                to_add_ids.append(new_id)
        #apply changes
        if len(ids_to_del) > 0:
            for id in ids_to_del:
                del_index = -1
                for i in range(len(role.feature_permissions)):
                    if role.feature_permissions[i].id == id:
                        del_index = i
                        need_commit = True
                        break
                if del_index >= 0:
                    del role.feature_permissions[del_index]
            #need_commit = True
        if len(to_add_ids) > 0:
            objects_to_add = self.db.session.query(FeaturePermission)\
                .filter(FeaturePermission.id.in_(to_add_ids))
            role.feature_permissions.extend(objects_to_add)
            need_commit = True
        if need_commit:
            self.db.session.commit()
            return role
        else:
            class_name = existed_feature.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_role_perms')

    def update_user_roles(self, user_id, roles_id):
        '''
        user_id - id
        roles_id - list of roles id
        '''
        user = self.warh_common.get_user(id=user_id)
        user_roles = user.roles
        #items to delete
        ids_to_delete = []
        for role in user_roles:
            is_not_found = True
            for new_id in roles_id:
                if role.id == new_id:
                    is_not_found = False
                    break
            if is_not_found:
                ids_to_delete.append(role.id)
        #add
        to_add_ids = []
        for new_id in roles_id:
            is_not_found = True
            for role in user_roles:
                if role.id == new_id:
                    is_not_found = False
                    break
            if is_not_found:
                to_add_ids.append(new_id)
        #apply changes
        if len(ids_to_delete) > 0:
            for id in ids_to_delete:
                del_index = -1
                for i in range(len(user_roles)):
                    if user_roles[i].id == id:
                        del_index = i
                        need_commit = True
                        break
                if del_index >= 0:
                    del user_roles[del_index]
        if len(to_add_ids) > 0:
            obj_list = []
            for id in to_add_ids:
                role_obj = self.warh_common.get_role(id=id)
                if role_obj is None:
                    raise ex.NotExistsError('Role', 'id', id)
                obj_list.append(role_obj)
                need_commit = True
            user.roles.extend(obj_list)
        if need_commit:
            self.db.session.commit()
            return user
        else:
            class_name = user.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_user_roles')
    #endregion Role permissions