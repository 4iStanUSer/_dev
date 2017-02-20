import json
import os
import sys
import transaction
from iap.common.repository.models.access import Project, Tool
from pyramid.paster import (get_appsettings, setup_logging)
from pyramid.scripts.common import parse_vars
from templates.access_rights_data import perm_data
from templates.dev_template import dev_template_JJOralCare, dev_template_JJLean
from iap.common.repository.models_managers.admin_manager import IManageAccess
from iap.common.repository.models_managers import scenario_manager as scenario_manager
from iap.common.repository.models.scenarios import Scenario
from iap.common.repository.models.access import User, Role, Feature, Tool, DataPermission, Permission
from iap.common.repository.models.warehouse import Entity
from iap.common.repository.models_managers.warehouse import Warehouse
from iap.data_loading.data_loader import Loader
from .db import (get_engine, get_session_factory, get_tm_session)
from .db.meta import Base
from ..repository import persistent_storage
from ...forecasting.workbench import Workbench


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def load_dev_templates(settings, project_name):
    """
    Load dev template form json

    :return:
    :rtype:

    """
    #Load json file
    base_path = settings['path.templates']
    template_path = os.path.join(base_path, "{0}.json".format(project_name)).replace("\\", "/")
    file = open(template_path).read()
    template = json.loads(file)

    return template


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings, prefix='sqlalchemy.')

    session_factory = get_session_factory(engine)

    with transaction.manager:

        ssn = get_tm_session(session_factory, transaction.manager)

        # Drop all tables
        Base.metadata.drop_all(engine)
        # Create all tables
        Base.metadata.create_all(engine)
        # Add root to entities tree.

        root = Entity(_name='root', _layer='root', _dimension_name='root')
        ssn.add(root)

        transaction.manager.commit()


        wh = Warehouse(session_factory)
        loader = Loader(wh)
        #loader.run_processing('JJLean')
        loader.run_processing('JJOralCare')

        transaction.manager.commit()

        imanage_access = IManageAccess(ssn=ssn)

        #Add Tool
        tool = imanage_access.add_tool(name='Forecasting', description='This is forecasting')
        tool.id = "forecast"


        #Add Projects
        project_1 = imanage_access.add_project(name='Oral Care Forecasting', description="This is JJOralCare Project")
        project_1.id = "JJOralCare"
        imanage_access.add_tool_to_project(tool, project_1)

        project_2 = imanage_access.add_project(name='Lean Forecasting', description="This is JJLean Project")
        project_2.id = "JJLean"
        imanage_access.add_tool_to_project(tool, project_2)



        #Add role's and connect it to tools
        role_forecast = Role(name="forecaster")
        imanage_access.add_role_to_tool(role=role_forecast, tool=tool)

        role_superviser = Role(name="superviser")
        imanage_access.add_role_to_tool(role=role_superviser, tool=tool)



        # Add  user@mail.com User for Project #1
        email = "user@mail.com"
        password = "qweasdZXC"
        user_1 = imanage_access.add_user(email=email, password=password)
        imanage_access.add_role_to_user(user_1, role_forecast)

        # Add default_user User for Project #2
        email = "default_user"
        password = "123456"
        user_2 = imanage_access.add_user(email=email, password=password)
        imanage_access.add_role_to_user(user_2, role_superviser)

        email = "user_2"
        password = "123456"
        user_3 = imanage_access.add_user(email=email, password=password)
        imanage_access.add_role_to_user(user_3, role_forecast)


        #Add roles Forecaster and set that feature
        features = ['create', 'view', 'finalize', 'edit', 'delete', 'edit', 'share']
        for feature in features:
            imanage_access.add_feature(name=feature, tool=tool, role=role_forecast)

        # Add Roles Superviser and set that feature
        features = ['create', 'view', 'publish', 'finalize', 'modify', 'include', 'edit', 'delete',
                    'share', 'copy']
        for feature in features:
            imanage_access.add_feature(name=feature, tool=tool, role=role_superviser)


        #Add data permission:
        permission = imanage_access.create_permission(name="Development Template")

        for data in perm_data["JJLean"]:

            data_permission = imanage_access.create_data_permision(project="JJLean",
                                                                   in_path=data['in_path'],
                                                                   out_path=data['out_path'],
                                                                   mask=data['mask'])

            imanage_access.add_data_permission_to_permission(permission, data_permission)

        imanage_access.add_permission_to_user(user_1, permission)


        for data in perm_data["JJOralCare"]:
            data_permission = imanage_access.create_data_permision(project="JJOralCare",
                                                                   in_path=data['in_path'],
                                                                   out_path=data['out_path'],
                                                                   mask=data['mask'])
            imanage_access.add_data_permission_to_permission(permission, data_permission)

        imanage_access.add_permission_to_user(user_2, permission)



        #Add Scenario
        input_data_1 = dict(name="Price Growth Dynamics JJOralCare", description="Dynamics of Price Growth in Brazil",
                            status="Final", shared="Yes", criteria="Brazil-Nike-Main", author=user_1.email,
                          )

        input_data_2 = dict(name="Price Growth Dynamics JJLean", description="Dynamics of Price Growth in USA",
                              status="Draft", shared="No", criteria="USA-iPhone-Main", author=user_2.email,
                            )

        for i in range(11):
            scenario = scenario_manager.create_scenario(ssn, user=None, input_data=input_data_1)
            scenario.users = [user_1, user_2, user_3]
            scenario = scenario_manager.create_scenario(ssn, user=None, input_data=input_data_2)
            scenario.users = [user_1, user_2]
        #TODO realise add user to scenario

        transaction.manager.commit()




        #Add Project and tool

        """
        Fill Persistance storage

        """

        #TODO admin manager add

        user_id = 2#user.email
        tool_id = 'forecast'
        project_id = 'JJOralCare'
        #wb = Workbench(user_id)
        #wb.init_load(wh, dev_template_JJLean)
        #backup = wb.get_backup()
        #persistent_storage.save_backup(user_id, tool_id, 'JJLean', backup)

        wb = Workbench(user_id)
        template = load_dev_templates(settings, "JJOralCare")
        user_access_rights = {"features": template['features'],
                              "entities": template['user_data_access']}
        wb.initial_load(wh, template, dev_template_JJOralCare['calc_instructions'], user_access_rights)
        backup = wb.get_backup()

        persistent_storage.save_backup(user_id, tool_id, project_id, backup, backup_name='default')


        project_id = "JJLean"
        template = load_dev_templates(settings, "JJLean")
        user_access_rights = {"features": template['features'],
                              "entities": template['user_data_access']}

        wb.initial_load(wh, template, dev_template_JJLean['calc_instructions'], user_access_rights)
        backup = wb.get_backup()

        persistent_storage.save_backup(user_id, tool_id, project_id, backup, backup_name='default')




        # Add tools

        #transaction.manager.commit()

        tool_forecast = imanage_access.get_tool(name='Forecasting')
        f_tool_id = tool_forecast.id

        # Add roles
        print("Tool id", f_tool_id)
        role_jj_admin = imanage_access.add_role(name='jj_role_admin', tool_id=f_tool_id)
        role_jj_manager = imanage_access.add_role('jj_role_manager', f_tool_id)

        #transaction.manager.commit()

        role_jj_admin = imanage_access.get_role(name='jj_role_admin')
        role_jj_manager = imanage_access.get_role(name='jj_role_manager')

        role_admin_id = role_jj_admin.id
        role_manager_id = role_jj_manager.id

        # Add users
        user_jj_admin = imanage_access.add_user('jj_admin@gmail.com',
                                                'pass', [role_admin_id])
        user_jj_manager = imanage_access.add_user('jj_manager@gmail.com',
                                                  'pass', [role_manager_id])

        #transaction.manager.commit()

        user_jj_admin = imanage_access.get_user(email='jj_admin@gmail.com')
        user_admin_id = user_jj_admin.id

        #imanage_access.set_permissions_template(f_tool_id, tool_template)

        #imanage_access.init_user_wb(f_tool_id, user_admin_id)
        # imanage_access.update_user_data_permissions(1, 1, permissions)

        #transaction.manager.commit()

        features = imanage_access.get_features(f_tool_id)
        imanage_access.update_role_features(role_admin_id,
                                            [f.id for f in features])

        #transaction.manager.commit()
