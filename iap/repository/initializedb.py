import os
import sys
import json
import transaction
import json
from pyramid.paster import (get_appsettings, setup_logging)
from pyramid.scripts.common import parse_vars
from iap.data_loading.data_loader import Loader
from iap.repository.tmp_template import tool_template
from .db import (get_engine, get_session_factory, get_tm_session)
from .db.meta import Base
from .db.warehouse import Entity, Warehouse
from .db.models import Project,Pr_Tool
from .db.models_access import Scenario, User, Role, Feature, Tool, DataPermission, Permission

from ..repository.interface.imanage_access import IManageAccess

from ..repository import persistent_storage
from ..forecasting.workbench import Workbench
from ..common.dev_template import dev_template_JJLean, dev_template_JJOralCare


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)




def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    #get path to .ini file
    options = parse_vars(argv[2:])
    #get parameters ~ options
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
        from .db.models import Project, Pr_Tool
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

        #Add  user@mail.com User
        email = "user@mail.com"
        password = "qweasdZXC"
        user_1 = User(email=email, password=password)

        # Add default_user User
        email = "default_user"
        password = "123456"
        user_2 = User(email=email, password=password)

        #Add Roles Forecaster
        features = ['Create a new scenario', 'View Scenario', 'Mark scenario as final']
        tool = Tool(name="Forecasting")
        role_forecast = Role(name="forecaster")
        tool.roles.append(role_forecast)

        for feature in features:
            role_forecast.features.append(Feature(name=feature))

        # Add Roles Superviser
        features = ['Create a new scenario', 'View Scenario', 'Publish Scenario', 'Mark scenario as final',
                    'Include Scenario']
        role_superviser = Role(name="superviser")

        for feature in features:
            role_superviser.features.append(Feature(name=feature))
        role_admin = Role(name="admin")

        #Commit

        user_1.roles.append(role_superviser)
        user_1.roles.append(role_admin)
        ssn.add(user_1)

        user_2.roles.append(role_forecast)
        ssn.add(user_2)
        transaction.manager.commit()

        #Add data permission:
        from .access_rights_data import perm_data

        permission = Permission("Development Template")
        projects = perm_data.keys()
        for project in projects:
            for data in perm_data[project]:
                data_permission = DataPermission(project=project, in_path=data['in_path'],
                                                 out_path=data['out_path'],mask=data['mask'])
                permission.data_perm.append(data_permission)
                ssn.add(data_permission)

        #Set Permission for User
        user_1.perms.append(permission)
        transaction.manager.commit()

        #Add Scenario
        scenario = Scenario(name="Price Growth Dynamics", description="Dynamics of Price Growth in Brazil",
                            status="New",shared="No",criteria="Brazil-Nike-Main")
        user_1.scenarios.append(scenario)
        transaction.manager.commit()


        user_id = '111'
        tool_id = 'forecast'
        #wb = Workbench(user_id)
        #wb.init_load(wh, dev_template_JJLean)
        #backup = wb.get_backup()
        #persistent_storage.save_backup(user_id, tool_id, 'JJLean', backup)

        wb = Workbench(user_id)
        wb.initial_load(wh, dev_template_JJOralCare, None)
        backup = wb.get_backup()
        persistent_storage.save_backup(user_id, tool_id, 'JJOralCare', backup)



        imanage_access = IManageAccess(ssn=ssn)
        # Add tools
        tool_forecast = imanage_access.add_tool('Forecast')
        tool_ppt = imanage_access.add_tool('PPT')
        tool_mmm = imanage_access.add_tool('MMM')

        transaction.manager.commit()

        tool_forecast = imanage_access.get_tool(name='Forecast')
        f_tool_id = tool_forecast.id

        # Add roles
        role_jj_admin = imanage_access.add_role('jj_role_admin',
                                                f_tool_id)
        role_jj_manager = imanage_access.add_role('jj_role_manager',
                                                  f_tool_id)

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

        imanage_access.set_permissions_template(f_tool_id, tool_template)

        imanage_access.init_user_wb(f_tool_id, user_admin_id)
        # imanage_access.update_user_data_permissions(1, 1, permissions)

        transaction.manager.commit()

        features = imanage_access.get_features(f_tool_id)
        imanage_access.update_role_features(role_admin_id,
                                            [f.id for f in features])

        transaction.manager.commit()
