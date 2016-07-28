'''
DB Pakage works directly with database via interface.
db_connector is instance of base connection to data base.
warh_... instances of warehouse managers.
'''
'''
from .db_connector import DBConnector
from .warehouse_common import WarehouseCommon
from .warehouse_access import WarehouseAccess
from IAP.repository.services.access_service import AccessService 

db_connector = DBConnector()
warh_common = WarehouseCommon(db_connector)
warh_access = WarehouseAccess(db_connector, warh_common)
access_service = AccessService(warh_common)


def user_manipulations():
    try:
        #region Clients
        new_client = warh_common.add_client('Client4','Code4')
        #endregion Clients

        #region Users
        new_user = warh_common.add_user('user4@gmail.com', 'pass4', new_client)
        #endregion Users

        #region Roles    
        new_role = warh_common.add_role('TestRole1', new_client)
        new_role2 = warh_common.add_role('TestRole2', new_client)
        new_role3 = warh_common.add_role('TestRole3', new_client)
        #endregion Roles

        #region Project manipulations
        new_project = warh_common.add_project('TestProj3', 'Some Test Project3', 'tsproj3', new_client)
        #endregion Project manipulations

        #Timescales
        new_ts = warh_common.add_timescale('New TimeScale1', new_project)
        #endregion Timescales

        #region Tools
        new_tool1 = warh_common.add_tool('Tool1')
        #endregion Tools

        #region Features
        new_feature1 = warh_common.add_feature(new_tool1,'Feature1', ['a', 'b', 'c'])
        new_feature2 = warh_common.add_feature(new_tool1,'Feature2', ['d', 'e', 'c'])
        #endregion Features

        #region user perms
        new_role_perm1 = warh_access.add_perms_to_role(new_role, new_feature1.permissions)
        new_role_perm2 = warh_access.add_perms_to_role(new_role2, new_feature2.permissions)

        #add user permissions
        new_user.roles.append(new_role)
        new_user.roles.append(new_role2)
        db_connector.session.commit()
        print (new_user.roles[0].feature_permissions)

        some_user = warh_access.update_user_roles(new_user.id, 
                                                  [new_role.id, new_role3.id])

        #endregion user perms
        print('something')
    #except NameError as err:
    #    print(err.args)
    #except ValueError as err:
    #    print(err.args)
    except Exception as err:
        print('Exception')
        print(err.args)

def services_manipulations(access_service, warh_common):
    user1 = warh_common.get_user(email='user4@gmail.com')
    user_perms = access_service.get_user_permissions(user1)
    print (user_perms)

def test():
       #region Clients
        new_client = warh_common.add_client('Client4','Code4')
        update_client = warh_common.update_client(new_client.id, 'Client5', 'Code5')
        warh_common.delete_client(update_client.id)
        new_client2 = warh_common.add_client('Client4','Code4')
        existed_client = warh_common.get_client(id = new_client2.id)
        print(new_client2.name)
        #endregion Clients

        #region Users
        new_user = warh_common.add_user('user4@gmail.com', 'pass4', existed_client)
        update_user = warh_common.update_user(new_user.id, 'user4@gmail.com', 'pass5')
        warh_common.delete_user(new_user.id,)
        new_user2 = warh_common.add_user('user44@gmail.com', 'pass44', existed_client)
        user_by_id = warh_common.get_user(id = new_user2.id)
        print(user_by_id.email)
        #endregion Users

        #region Roles    
        new_role = warh_common.add_role('TestRole1', existed_client)
        update_role = warh_common.update_role(new_role.id, 'TestRole1 Updated')
        delete_role = warh_common.delete_role(update_role.id)
        new_role2 = warh_common.add_role('TestRole2', existed_client)
        get_role = warh_common.get_role(name='TestRole2', client_id=existed_client.id)
        #endregion Roles

        #region Project manipulations
        new_project = warh_common.add_project('TestProj3', 'Some Test Project3', 'tsproj3', existed_client)
        update_project = warh_common.update_project(new_project.id, 'TestProj3 Updated', 'Some Test Project3', 'tsproj3u')
        warh_common.delete_project(update_project.id)
        new_project2 = warh_common.add_project('TestProj4', 'Some Test Project4', 'tsproj4', existed_client)
        #endregion Project manipulations

        #Timescales
        new_ts = warh_common.add_timescale('New TimeScale1', new_project2)
        update_ts = warh_common.update_timescale(new_ts.id, 'New TS1 Updated')
        delete_ts = warh_common.delete_timescale(new_ts.id)
        #endregion Timescales

        #region Tools
        new_tool1 = warh_common.add_tool('Tool1')
        update_tool1 = warh_common.update_tool(new_tool1.id, 'Tool1 Update')
        get_tool1 = warh_common.get_tool(name = 'Tool1 Update')
        warh_common.delete_tool(new_tool1.id)
        new_tool2 = warh_common.add_tool('Tool2')
        #endregion Tools

        #region Features
        new_feature1 = warh_common.add_feature(new_tool2,'Feature1', ['a', 'b', 'c'])
        update_feature1 = warh_common.update_feature(new_feature1.id, 'Feature1 Update', ['c', 'd', 'e'])
        get_feature1 = warh_common.get_feature(name = 'Feature1 Update', tool_id = new_tool2.id)
        warh_common.delete_feature(get_feature1.id)
        new_feature2 = warh_common.add_feature(new_tool2,'Feature2', ['e', 'f', 'g'])
        #endregion Features

        #region user perms
        new_role_perm1 = warh_access.add_perms_to_role(new_role2, new_feature2.permissions)
        get_role_perm1 = warh_access.get_role_perms(new_role_perm1)
        new_role_perm1 = warh_access.update_role_perms(new_role2, [6, 7])

'''

