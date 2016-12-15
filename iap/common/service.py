from iap.repository.db.models_access import User





# def _get_ssn(req):
#     return req.dbsession


def get_user_by_id(id):
    """Get user by id

    :param id:
    :type id:
    :return:
    :rtype:

    """
    users = [{"id": 1, "login": 'default_user', 'password': '123456'},
    {"id": 2, "login": 'user_1', 'password':'12345'},
    {"id": 3, "login": 'user_2', 'password':'12345'},
    {"id": 4, "login": 'user_3', 'password':'12345'}]
    for user in users:
        if user["id"] == id:
            return user
    return None


def check_password(login, password):
    users = [{"id": 1, "login": 'default_user', 'password': '123456'},
             {"id": 2, "login": 'user_1', 'password': '12345'},
             {"id": 3, "login": 'user_2', 'password': '12345'},
             {"id": 4, "login": 'user_3', 'password': '12345'}]
    for user in users:
        if user["login"] == login and user['password'] == password:
            return user
    return None


def get_user_by_email(email):
    return None


# def fillin_db(req):
#     ssn = _get_ssn(req)
#
#     with transaction.manager:
#         # Add tools
#         tool_forecast = imanage_access.add_tool(ssn, 'Forecast')
#         tool_ppt = imanage_access.add_tool(ssn, 'PPT')
#         tool_mmm = imanage_access.add_tool(ssn, 'MMM')
#
#         transaction.manager.commit()
#
#         tool_forecast = imanage_access.get_tool(ssn, name='Forecast')
#         f_tool_id = tool_forecast.id
#
#         # Add roles
#         role_jj_admin = imanage_access.add_role(ssn, 'jj_role_admin',
#                                                 f_tool_id)
#         role_jj_manager = imanage_access.add_role(ssn, 'jj_role_manager',
#                                                   f_tool_id)
#
#         transaction.manager.commit()
#
#         role_jj_admin = imanage_access.get_role(ssn, name='jj_role_admin')
#         role_jj_manager = imanage_access.get_role(ssn, name='jj_role_manager')
#
#         role_admin_id = role_jj_admin.id
#         role_manager_id = role_jj_manager.id
#
#         # Add users
#         user_jj_admin = imanage_access.add_user(ssn, 'jj_admin@gmail.com',
#                                                 'pass', [role_admin_id])
#         user_jj_manager = imanage_access.add_user(ssn, 'jj_manager@gmail.com',
#                                                   'pass', [role_manager_id])

# def init_user_wb(req, tool_id, user_id):
#     ssn = _get_ssn(req)
#     with transaction.manager:
#         return imanage_access.init_user_wb(ssn, tool_id, user_id)
#
#
# def get_permissions(req, tool_id, user_id):
#     ssn = _get_ssn(req)
#     return iaccess.get_permissions(ssn, tool_id, user_id)
#
#
# def update_user_perms(req):
#     ssn = _get_ssn(req)
#     permissions = [
#         {
#             'mask': 9,
#             'path': ['Argentina', 'Chocolate'],
#             'name': 'Praline',
#             'node_type': 'ent'
#         },
#         {
#             'mask': 7,
#             'path': ['Argentina', 'Chocolate', 'Praline'],
#             'name': 'Unit',
#             'node_type': 'var'
#         },
#         {
#             'mask': 5,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit'],
#             'name': 'Quarterly',
#             'node_type': 'ts'
#         },
#         {
#             'mask': 4,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit'],
#             'name': 'Annual',
#             'node_type': 'ts'
#         },
#         {
#             'mask': 3,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit',
#                      'Annual'],
#             'name': '2014',
#             'node_type': 'tp'
#         },
#         {
#             'mask': 2,
#             'path': ['Argentina', 'Chocolate', 'Praline',
#                      'Unit',
#                      'Annual'],
#             'name': '2015',
#             'node_type': 'tp'
#         },
#         {
#             'mask': 6,
#             'path': ['Argentina', 'Chocolate', 'Praline'],
#             'name': 'Dollars',
#             'node_type': 'var'
#         },
#         {
#             'mask': 8,
#             'path': ['Brazil', 'Chocolate'],
#             'name': 'Praline',
#             'node_type': 'ent'
#         },
#         {
#             'mask': 1,
#             'path': ['Brazil', 'Chocolate', 'Praline', 'Unit', 'Annual'],
#             'name': '2015',
#             'node_type': 'tp'
#
#         },
#     ]
#
#     with transaction.manager:
#         imanage_access.update_user_data_permissions(ssn, 1, 1, permissions)
#
#
# def set_permissions_template(req):
#     ssn = _get_ssn(req)
#
#     structure = {
#         'features': [
#             {
#                 'name': 'new_view_feature'
#             },
#             {
#                 'name': 'new_edit_feature',
#             },
#         ],
#         'permissions': [
#             {
#                 'mask': 999,
#                 'path': ['Argentina', 'Chocolate'],
#                 'name': 'Praline',
#                 'node_type': 'ent'
#             },
#             {
#                 'mask': 997,
#                 'path': ['Argentina', 'Chocolate', 'Praline'],
#                 'name': 'Unit',
#                 'node_type': 'var'
#             },
#             {
#                 'mask': 995,
#                 'path': ['Argentina', 'Chocolate', 'Praline', 'Unit'],
#                 'name': 'Quarterly',
#                 'node_type': 'ts'
#             },
#             {
#                 'mask': 994,
#                 'path': ['Argentina', 'Chocolate', 'Praline', 'Unit'],
#                 'name': 'Annual',
#                 'node_type': 'ts'
#             },
#             {
#                 'mask': 993,
#                 'path': ['Argentina', 'Chocolate', 'Praline', 'Unit',
#                          'Annual'],
#                 'name': '2014',
#                 'node_type': 'tp'
#             },
#             {
#                 'mask': 992,
#                 'path': ['Argentina', 'Chocolate', 'Praline', 'Unit',
#                          'Annual'],
#                 'name': '2015',
#                 'node_type': 'tp'
#             },
#             {
#                 'mask': 996,
#                 'path': ['Argentina', 'Chocolate', 'Praline'],
#                 'name': 'Dollars',
#                 'node_type': 'var'
#             },
#             {
#                 'mask': 998,
#                 'path': ['Brazil', 'Chocolate'],
#                 'name': 'Praline',
#                 'node_type': 'ent'
#
#             },
#         ],
#     }
#
#     with transaction.manager:
#         return imanage_access.set_permissions_template(ssn, 1, structure)
