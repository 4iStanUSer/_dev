import os
import sys
import transaction

from pyramid.paster import (get_appsettings, setup_logging)

from pyramid.scripts.common import parse_vars
from sqlalchemy import MetaData

from .warehouse.meta import Base
from .warehouse import (get_engine, get_session_factory, get_tm_session,
                        wh_common, wh_access)


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
        sess = get_tm_session(session_factory, transaction.manager)

        # TODO remove procedure of removing all rows
        # Drop all tables
        Base.metadata.drop_all(engine)
        # Create all tables
        Base.metadata.create_all(engine)

        """
        #sess.autoflush = False #???????

        # TODO add db init fill here
        client = wh_common.add_client(sess, 'Jonson', 'JJ')

        # Add roles
        role_jj_admin = wh_access.add_role(sess, 'jj_role_admin', client)
        role_jj_manager = wh_access.add_role(sess, 'jj_role_manager', client)

        # Add users
        user_jj_admin = wh_access.add_user(sess, 'jj_admin@gmail.com', 'pass')
        wh_access.add_role_to_user(sess, user_jj_admin, role_jj_admin)
        wh_access.add_role_to_user(sess, user_jj_admin, role_jj_manager)
        user_jj_manager = wh_access.add_user(sess, 'jj_manager@gmail.com',
                                             'pass', role_jj_manager)

        # Add tools
        tool_forecast = wh_access.add_tool(sess, 'Forecast')
        tool_ppt = wh_access.add_tool(sess, 'PPT')
        tool_mmm = wh_access.add_tool(sess, 'MMM')

        # Add features
        feature_view_drv = wh_access.add_feature(sess, 'view_driver',
                                                 tool_forecast)
        feature_view_sce = wh_access.add_feature(sess,
                                                 'view_scenario',
                                                 tool_forecast)
        feature_view_coef = wh_access.add_feature(sess,
                                                  'view_coefficient',
                                                  tool_forecast)
        feature_edit_drv = wh_access.add_feature(sess, 'edit_driver',
                                                 tool_forecast)
        feature_edit_sce = wh_access.add_feature(sess,
                                                 'edit_scenario',
                                                 tool_forecast)
        feature_edit_coef = wh_access.add_feature(sess,
                                                  'edit_coefficient',
                                                  tool_forecast)

        wh_access.add_feature_to_role(sess, role_jj_admin, feature_view_drv)
        wh_access.add_feature_to_role(sess, role_jj_admin, feature_view_sce)
        wh_access.add_feature_to_role(sess, role_jj_admin, feature_view_coef)
        wh_access.add_feature_to_role(sess, role_jj_admin, feature_edit_drv)
        wh_access.add_feature_to_role(sess, role_jj_admin, feature_edit_sce)
        wh_access.add_feature_to_role(sess, role_jj_admin, feature_edit_coef)
        wh_access.add_feature_to_role(sess, role_jj_manager, feature_view_drv)
        wh_access.add_feature_to_role(sess, role_jj_manager, feature_view_sce)
        wh_access.add_feature_to_role(sess, role_jj_manager, feature_view_coef)

        transaction.manager.commit()

        # Add permissions
        tool_forecast = wh_access.get_tool(sess, name='Forecast')
        tool_ppt = wh_access.get_tool(sess, name='PPT')
        user_jj_admin = wh_access.get_user(sess, id=1)
        user_jj_manager = wh_access.get_user(sess, id=2)

        node_ent_1 = wh_access.add_perm_node(sess, 'ent')
        node_ent_2 = wh_access.add_perm_node(sess, 'ent')
        node_var_1_1 = wh_access.add_perm_node(sess, 'var', node_ent_1)
        node_var_1_2 = wh_access.add_perm_node(sess, 'var', node_ent_1)
        node_ts_1_1_1 = wh_access.add_perm_node(sess, 'ts', node_var_1_1)
        node_ts_1_1_2 = wh_access.add_perm_node(sess, 'ts', node_var_1_1)
        node_tp_1_1_1 = wh_access.add_perm_node(sess, 'tp', node_ts_1_1_1)
        node_tp_1_1_2 = wh_access.add_perm_node(sess, 'tp', node_ts_1_1_1)

        wh_access.add_perm_node_to_tool(sess, node_ent_1, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_ent_2, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_var_1_1, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_var_1_2, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_ts_1_1_1, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_ts_1_1_2, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_tp_1_1_1, tool_forecast)
        wh_access.add_perm_node_to_tool(sess, node_tp_1_1_2, tool_forecast)

        wh_access.add_perm_value(sess, node_ent_1, 99, user_jj_admin)
        wh_access.add_perm_value(sess, node_ent_2, 98, user_jj_admin)
        wh_access.add_perm_value(sess, node_var_1_1, 97, user_jj_admin)
        wh_access.add_perm_value(sess, node_var_1_2, 96, user_jj_admin)
        wh_access.add_perm_value(sess, node_ts_1_1_1, 95, user_jj_admin)
        wh_access.add_perm_value(sess, node_ts_1_1_2, 94, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_1, 93, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_2, 92, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_1, 10, user_jj_manager)
        wh_access.add_perm_value(sess, node_tp_1_1_2, 9, user_jj_manager)

        wh_access.add_perm_node_to_tool(sess, node_ent_1, tool_ppt)
        wh_access.add_perm_node_to_tool(sess, node_ent_2, tool_ppt)
        wh_access.add_perm_node_to_tool(sess, node_var_1_1, tool_ppt)
        wh_access.add_perm_node_to_tool(sess, node_var_1_2, tool_ppt)
        wh_access.add_perm_node_to_tool(sess, node_ts_1_1_1, tool_ppt)
        wh_access.add_perm_node_to_tool(sess, node_ts_1_1_2, tool_ppt)
        # wh_access.add_perm_node_to_tool(sess, node_tp_1_1_1, tool_ppt)
        # wh_access.add_perm_node_to_tool(sess, node_tp_1_1_2, tool_ppt)

        # node1_ent_1 = wh_access.add_perm_node(sess, tool_ppt, 'ent')
        # node1_ent_2 = wh_access.add_perm_node(sess, tool_ppt, 'ent')
        #
        # node1_var_1_1 = wh_access.add_perm_node(sess, tool_ppt, 'var',
        #                                         node1_ent_1)
        # node1_var_1_2 = wh_access.add_perm_node(sess, tool_ppt, 'var',
        #                                         node1_ent_1)
        #
        # node1_ts_1_1_1 = wh_access.add_perm_node(sess, tool_ppt, 'ts',
        #                                          node1_var_1_1)
        # node1_ts_1_1_2 = wh_access.add_perm_node(sess, tool_ppt, 'ts',
        #                                          node1_var_1_1)
        #
        # node1_tp_1_1_1 = wh_access.add_perm_node(sess, tool_ppt, 'tp',
        #                                          node1_ts_1_1_1)
        # node1_tp_1_1_2 = wh_access.add_perm_node(sess, tool_ppt, 'tp',
        #                                          node1_ts_1_1_1)

        wh_access.add_perm_value(sess, node_ent_1, 999, user_jj_admin)
        wh_access.add_perm_value(sess, node_ent_2, 998, user_jj_admin)
        wh_access.add_perm_value(sess, node_var_1_1, 997, user_jj_admin)
        wh_access.add_perm_value(sess, node_var_1_2, 996, user_jj_admin)
        wh_access.add_perm_value(sess, node_ts_1_1_1, 995, user_jj_admin)
        wh_access.add_perm_value(sess, node_ts_1_1_2, 994, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_1, 993, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_2, 992, user_jj_admin)
        wh_access.add_perm_value(sess, node_tp_1_1_1, 910, user_jj_manager)
        wh_access.add_perm_value(sess, node_tp_1_1_2, 909, user_jj_manager)

        # Do global commit
        transaction.manager.commit()

        # tool = wh_access.get_tool(sess, name='Forecast')
        # user = wh_access.get_user(sess, id=2)
        # perms = wh_access.get_user_perms_to_forecast_tool(sess, tool, user)
        #
        # print(perms)

        # entity1 = wh_access.add_permission(sess, 1, 'entity', 15)
        # entity2 = wh_access.add_permission(sess, 2, 'entity', 25)
        #
        # variable1_1 = wh_access.add_permission(sess, 11, 'variable', 25,
        #                                        entity1)
        # variable1_2 = wh_access.add_permission(sess, 12, 'variable', 26,
        #                                        entity1)
        #
        # variable2_1 = wh_access.add_permission(sess, 13, 'variable', 5,
        #                                        entity2)
        #
        # timeseries1_1_1 = wh_access.add_permission(sess, 101, 'timeseries', 20,
        #                                            variable1_1)
        # timeseries1_1_2 = wh_access.add_permission(sess, 102, 'timeseries', 19,
        #                                            variable1_1)
        #
        # timepoint1_1_1_1 = wh_access.add_permission(sess, 1001, 'timepoint',
        #                                             18, timeseries1_1_1)
        # timepoint1_1_1_2 = wh_access.add_permission(sess, 1002, 'timepoint',
        #                                             17, timeseries1_1_1)
        #

        #
        # Add features permissions
        # TODO Question about relations between f_perm & role (not user_role)
        # #for admin role
        # f_perm_adm_driv_view = wh_access.add_f_permission(sess, 'view',
        #                                                   feature_driver,
        #                                                   role_jj_admin)
        # f_perm_adm_driv_edit = wh_access.add_f_permission(sess, 'edit',
        #                                                   feature_driver,
        #                                                   role_jj_admin)
        # f_perm_adm_sce_view = wh_access.add_f_permission(sess, 'view',
        #                                                  feature_scenario,
        #                                                  role_jj_admin)
        # f_perm_adm_sce_edit = wh_access.add_f_permission(sess, 'edit',
        #                                                  feature_scenario,
        #                                                  role_jj_admin)
        # #for manager role
        # f_perm_mng_driv_view = wh_access.add_f_permission(sess, 'view',
        #                                                   feature_driver,
        #                                                   role_jj_manager)
        # f_perm_mng_driv_edit = wh_access.add_f_permission(sess, 'edit',
        #                                                   feature_driver,
        #                                                   role_jj_manager)
        # f_perm_mng_sce_view = wh_access.add_f_permission(sess, 'view',
        #                                                  feature_scenario,
        #                                                  role_jj_manager)
        # f_perm_mng_sce_edit = wh_access.add_f_permission(sess, 'edit',
        #                                                  feature_scenario,
        #                                                  role_jj_manager)

        # TODO Add another values
        """
