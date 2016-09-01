import os
import sys
import transaction

from pyramid.paster import (get_appsettings, setup_logging)

from pyramid.scripts.common import parse_vars

from .db.meta import Base
from .db import (get_engine, get_session_factory, get_tm_session)
from .db.warehouse import Entity, Warehouse

from ..repository import imanage_access
from ..forecasting.template import tool_template
from iap.data_processing.data_proc_manager import Loader


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


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
        root = Entity(name='root', layer='root', dimension='root')
        ssn.add(root)

        transaction.manager.commit()

        wh = Warehouse(session_factory)
        loader = Loader(wh, data_load_command='jj')
        loader.load()

        transaction.manager.commit()

        # Add tools
        tool_forecast = imanage_access.add_tool(ssn, 'Forecast')
        tool_ppt = imanage_access.add_tool(ssn, 'PPT')
        tool_mmm = imanage_access.add_tool(ssn, 'MMM')

        transaction.manager.commit()

        tool_forecast = imanage_access.get_tool(ssn, name='Forecast')
        f_tool_id = tool_forecast.id

        # Add roles
        role_jj_admin = imanage_access.add_role(ssn, 'jj_role_admin',
                                                f_tool_id)
        role_jj_manager = imanage_access.add_role(ssn, 'jj_role_manager',
                                                  f_tool_id)

        transaction.manager.commit()

        role_jj_admin = imanage_access.get_role(ssn, name='jj_role_admin')
        role_jj_manager = imanage_access.get_role(ssn, name='jj_role_manager')

        role_admin_id = role_jj_admin.id
        role_manager_id = role_jj_manager.id

        # Add users
        user_jj_admin = imanage_access.add_user(ssn, 'jj_admin@gmail.com',
                                                'pass', [role_admin_id])
        user_jj_manager = imanage_access.add_user(ssn, 'jj_manager@gmail.com',
                                                  'pass', [role_manager_id])

        transaction.manager.commit()

        user_jj_admin = imanage_access.get_user(ssn,
                                                email='jj_admin@gmail.com')
        user_admin_id = user_jj_admin.id

        imanage_access.set_permissions_template(ssn, f_tool_id, tool_template)

        imanage_access.init_user_wb(ssn, f_tool_id, user_admin_id)
        # imanage_access.update_user_data_permissions(ssn, 1, 1, permissions)
