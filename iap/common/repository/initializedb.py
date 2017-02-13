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

        # TODO remove procedure of removing all rows
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


        tool = imanage_access.add_tool(name='Forecasting', description='This is forecasting')
        tool.id = "forecast"
        
        project_1 = imanage_access.add_project(name='Oral Care Forecasting', description="This is JJOralCare Project")
        project_1.id = "JJOralCare"
        project_1.tools.append(tool)

        project_2 = imanage_access.add_project(name='Lean Forecasting', description="This is JJLean Project")
        project_2.id = "JJLean"
        project_2.tools.append(tool)

        #Create Tool Forecating
        #Add  user@mail.com User for Project #1

        email = "user@mail.com"
        password = "qweasdZXC"
        user_1 = imanage_access.add_user(email=email, password=password)

        # Add default_user User for Project #2
        email = "default_user"
        password = "123456"
        user_2 = imanage_access.add_user(email=email, password=password)

        #Add roles and features

        #Add Roles Forecaster
        features = ['create', 'view', 'finalize', 'modify',
                    'delete']
        role_forecast = Role(name="forecaster")

        tool.roles.append(role_forecast)
        for feature in features:
            _feature = Feature(name=feature)
            tool.features.append(_feature)
            role_forecast.features.append(_feature)

        # Add Roles Superviser
        features = ['create', 'view', 'publish', 'finalize',
                    'modify', 'include']
        role_superviser = Role(name="superviser")
        tool.roles.append(role_superviser)
        for feature in features:
            _feature = Feature(name=feature)
            tool.features.append(_feature)
            role_superviser.features.append(_feature)

        #Add Roles
        user_1.roles.append(role_superviser)
        user_1.roles.append(role_forecast)

        user_2.roles.append(role_forecast)


        #Add data permission:

        permission = Permission(name="Development Template")

        for data in perm_data["JJLean"]:
            data_permission = DataPermission(project="JJLean", in_path=data['in_path'],
                                             out_path=data['out_path'], mask=data['mask'])
            permission.data_perms.append(data_permission)
            ssn.add(data_permission)

        permission = Permission(name="Development Template")

        for data in perm_data["JJLean"]:
            data_permission = DataPermission(project="JJLean", in_path=data['in_path'],
                                             out_path=data['out_path'], mask=data['mask'])
            permission.data_perms.append(data_permission)
            ssn.add(data_permission)

        user_1.perms.append(permission)

        for data in perm_data["JJOralCare"]:
            data_permission = DataPermission(project="JJOralCare", in_path=data['in_path'],
                                             out_path=data['out_path'],mask=data['mask'])
            permission.data_perms.append(data_permission)
            ssn.add(data_permission)

        #Set Permission for User #1
        user_2.perms.append(permission)

        #Add Scenario
        print("User_", user_1.email)
        input_data = dict(name="Price Growth Dynamics JJOralCare", description="Dynamics of Price Growth in Brazil",
                            status="New", shared="No", criteria="Brazil-Nike-Main", author=user_1.email)
        scenario_1 = scenario_manager.create_scenario(ssn, user_1,  input_data)
        #scenario_1 = Scenario(name="Price Growth Dynamics JJOralCare", description="Dynamics of Price Growth in Brazil",
        #                    status="New", shared="No", criteria="Brazil-Nike-Main", author=user_1.email)
        #user_1.scenarios.append(scenario_1)

        # Add Scenario
        input_data = dict(name="Price Growth Dynamics JJLean", description="Dynamics of Price Growth in USA",
                              status="New", shared="No", criteria="USA-iPhone-Main", author=user_2.email)
        scenario_2 = scenario_manager.create_scenario(ssn, user_2,  input_data)


        transaction.manager.commit()

        #Add Project and tool

        """
        Create table for storing information about projects and tools

        """



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

        transaction.manager.commit()

        tool_forecast = imanage_access.get_tool(name='Forecasting')
        f_tool_id = tool_forecast.id

        # Add roles
        print("Tool id", f_tool_id)
        role_jj_admin = imanage_access.add_role(name='jj_role_admin', tool_id=f_tool_id)
        role_jj_manager = imanage_access.add_role('jj_role_manager', f_tool_id)

        transaction.manager.commit()

        role_jj_admin = imanage_access.get_role(name='jj_role_admin')
        role_jj_manager = imanage_access.get_role(name='jj_role_manager')

        role_admin_id = role_jj_admin.id
        role_manager_id = role_jj_manager.id

        # Add users
        user_jj_admin = imanage_access.add_user('jj_admin@gmail.com',
                                                'pass', [role_admin_id])
        user_jj_manager = imanage_access.add_user('jj_manager@gmail.com',
                                                  'pass', [role_manager_id])

        transaction.manager.commit()

        user_jj_admin = imanage_access.get_user(email='jj_admin@gmail.com')
        user_admin_id = user_jj_admin.id

        #imanage_access.set_permissions_template(f_tool_id, tool_template)

        #imanage_access.init_user_wb(f_tool_id, user_admin_id)
        # imanage_access.update_user_data_permissions(1, 1, permissions)

        transaction.manager.commit()

        features = imanage_access.get_features(f_tool_id)
        imanage_access.update_role_features(role_admin_id,
                                            [f.id for f in features])

        transaction.manager.commit()
