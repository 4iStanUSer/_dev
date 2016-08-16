import transaction  # Temporary

from iap.repository import imanage_access, iaccess
from iap.repository.db import recreate_db  # TODO DELETE THIS


def get_user_by_id(id):
    return None  # warh_common.get_user(id=id) #TODO question


def get_user_by_email(email):
    return None  # warh_common.get_user(email=email) #TODO question


def init_permissions(req):
    sess = req.dbsession

    structure = {
        'features': [
            {
                'name': 'new_view_feature'
            },
            {
                'name': 'new_edit_feature',
            },
        ],
        'permissions': [
            {
                'mask': 999,
                'path': ['Argentina', 'Chocolate', 'Praline'],
                'node_type': 'ent'
            },
            {
                'mask': 998,
                'path': ['Brazil', 'Chocolate', 'Praline'],
                'node_type': 'ent'

            },
            {
                'mask': 997,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Unit'],
                'node_type': 'var'
            },
            {
                'mask': 996,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Dollars'],
                'node_type': 'var'
            },
            {
                'mask': 995,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Unit',
                         'Quarterly'],
                'node_type': 'ts'
            },
            {
                'mask': 994,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Unit',
                         'Annual'],
                'node_type': 'ts'
            },
            {
                'mask': 993,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Unit', 'Annual',
                         '2014'],
                'node_type': 'tp'
            },
            {
                'mask': 992,
                'path': ['Argentina', 'Chocolate', 'Praline', 'Unit', 'Annual',
                         '2015'],
                'node_type': 'tp'
            }
        ],
    }

    with transaction.manager:
        return imanage_access.init_permissions(sess, 1, structure)


def get_permissions(req):
    return iaccess.get_permissions(req, 1, 1)


def fillin_db(req):
    #recreate_db(req)

    sess = req.dbsession
    # Add tools
    with transaction.manager:
        tool_forecast = imanage_access.add_tool(sess, 'Forecast')
        tool_ppt = imanage_access.add_tool(sess, 'PPT')
        tool_mmm = imanage_access.add_tool(sess, 'MMM')

        # Add roles
        role_jj_admin = imanage_access.add_role(sess, 'jj_role_admin')
        role_jj_manager = imanage_access.add_role(sess, 'jj_role_manager')

        # Add users
        user_jj_admin = imanage_access.add_user(sess, 'jj_admin@gmail.com', 'pass')
        user_jj_manager = imanage_access.add_user(sess, 'jj_manager@gmail.com',
                                              'pass')

    # with transaction.manager:
    #     # Add tools
    #     tool_forecast = imanage_access.add_tool(sess, 'Forecast')
    #     tool_ppt = imanage_access.add_tool(sess, 'PPT')
    #     tool_mmm = imanage_access.add_tool(sess, 'MMM')
    #
    #     # Add roles
    #     role_jj_admin = imanage_access.add_role(sess, 'jj_role_admin')
    #     role_jj_manager = imanage_access.add_role(sess, 'jj_role_manager')
    #
    #     # Add users
    #     user_jj_admin = imanage_access.add_user(sess, 'jj_admin@gmail.com', 'pass')
    #     user_jj_manager = imanage_access.add_user(sess, 'jj_manager@gmail.com',
    #                                           'pass')
    #
    #     transaction.manager.commit()
    #
    #     # Get data objects
    #     tool_forecast = imanage_access.get_tool(sess, name='Forecast')
    #
    #     user_jj_admin = imanage_access.get_user(sess, email='jj_admin@gmail.com')
    #     user_jj_manager = imanage_access.get_user(sess,
    #                                           email='jj_manager@gmail.com')
    #
    #     role_jj_admin = imanage_access.get_role(sess, name='jj_role_admin')
    #     role_jj_manager = imanage_access.get_role(sess, name='jj_role_manager')
    #
    #     role_admin_id = role_jj_admin.id
    #     role_manager_id = role_jj_manager.id
    #     f_tool_id = tool_forecast.id
    #
    #     # Connect roles & tool
    #     imanage_access.add_role_to_tool(sess, role_admin_id, f_tool_id)
    #     imanage_access.add_role_to_tool(sess, role_manager_id, f_tool_id)
    #
    #     # Connect roles & users
    #     imanage_access.add_role_to_user(sess, user_jj_admin.id, role_admin_id)
    #     imanage_access.add_role_to_user(sess, user_jj_manager.id, role_manager_id)
    #
    #     transaction.manager.commit()
    #
    #     # Add features into tool
    #     imanage_access.add_feature(sess, 'view_driver', f_tool_id)
    #     imanage_access.add_feature(sess, 'view_scenario', f_tool_id)
    #     imanage_access.add_feature(sess, 'view_coefficient', f_tool_id)
    #     imanage_access.add_feature(sess, 'edit_driver', f_tool_id)
    #     imanage_access.add_feature(sess, 'edit_scenario', f_tool_id)
    #     imanage_access.add_feature(sess, 'edit_coefficient', f_tool_id)
    #
    #     transaction.manager.commit()
    #
    #     # Add features into user roles
    #     feature_view_drv = imanage_access.get_feature(sess, name='view_driver',
    #                                               tool_id=f_tool_id)
    #     feature_view_sce = imanage_access.get_feature(sess, name='view_scenario',
    #                                               tool_id=f_tool_id)
    #     feature_view_coef = imanage_access.get_feature(sess,
    #                                                name='view_coefficient',
    #                                                tool_id=f_tool_id)
    #     feature_edit_drv = imanage_access.get_feature(sess,
    #                                               name='edit_driver',
    #                                               tool_id=f_tool_id)
    #     feature_edit_sce = imanage_access.get_feature(sess,
    #                                               name='edit_scenario',
    #                                               tool_id=f_tool_id)
    #     feature_edit_coef = imanage_access.get_feature(sess,
    #                                                name='edit_coefficient',
    #                                                tool_id=f_tool_id)
    #
    #     imanage_access.add_feature_to_role(sess, feature_view_drv.id,
    #                                    role_manager_id)
    #     imanage_access.add_feature_to_role(sess, feature_view_sce.id,
    #                                    role_manager_id)
    #     imanage_access.add_feature_to_role(sess, feature_view_coef.id,
    #                                    role_manager_id)
    #
    #     imanage_access.add_feature_to_role(sess, feature_view_drv.id,
    #                                    role_admin_id)
    #     imanage_access.add_feature_to_role(sess, feature_view_sce.id,
    #                                    role_admin_id)
    #     imanage_access.add_feature_to_role(sess, feature_view_coef.id,
    #                                    role_admin_id)
    #     imanage_access.add_feature_to_role(sess, feature_edit_drv.id,
    #                                    role_admin_id)
    #     imanage_access.add_feature_to_role(sess, feature_edit_sce.id,
    #                                    role_admin_id)
    #     imanage_access.add_feature_to_role(sess, feature_edit_coef.id,
    #                                    role_admin_id)
    #
    #     # Add permissions
    #     node_ent_1 = imanage_access.add_permission(sess, f_tool_id, 'ent')
    #     node_ent_2 = imanage_access.add_permission(sess, f_tool_id, 'ent')
    #
    #     node_var_1_1 = imanage_access.add_permission(sess, f_tool_id, 'var',
    #                                              node_ent_1.id)
    #     node_var_1_2 = imanage_access.add_permission(sess, f_tool_id, 'var',
    #                                              node_ent_1.id)
    #
    #     node_ts_1_1_1 = imanage_access.add_permission(sess, f_tool_id, 'ts',
    #                                               node_var_1_1.id)
    #     node_ts_1_1_2 = imanage_access.add_permission(sess, f_tool_id, 'ts',
    #                                               node_var_1_1.id)
    #
    #     node_tp_1_1_1_1 = imanage_access.add_permission(sess, f_tool_id, 'tp',
    #                                                 node_ts_1_1_1.id)
    #     node_tp_1_1_1_2 = imanage_access.add_permission(sess, f_tool_id, 'tp',
    #                                                 node_ts_1_1_1.id)
    #
    #     user_jj_admin = imanage_access.get_user(sess, email='jj_admin@gmail.com')
    #     user_jj_manager = imanage_access.get_user(sess,
    #                                           email='jj_manager@gmail.com')
    #
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ent_1.id, 99,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ent_2.id, 98,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_var_1_1.id, 97,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_var_1_2.id, 96,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ts_1_1_1.id, 95,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ts_1_1_2.id, 94,
    #                                     user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_tp_1_1_1_1.id,
    #                                     93, user_jj_admin.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_tp_1_1_1_2.id,
    #                                     92, user_jj_admin.id)
    #
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ent_1.id, 9,
    #                                     user_jj_manager.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ent_2.id, 8,
    #                                     user_jj_manager.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_var_1_1.id, 7,
    #                                     user_jj_manager.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_var_1_2.id, 6,
    #                                     user_jj_manager.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ts_1_1_1.id, 5,
    #                                     user_jj_manager.id)
    #     imanage_access.add_permission_value(sess, f_tool_id, node_ts_1_1_2.id, 4,
    #                                     user_jj_manager.id)
