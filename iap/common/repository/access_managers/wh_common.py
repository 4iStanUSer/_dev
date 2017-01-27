from sqlalchemy import or_

from iap.common.repository import exceptions as ex


def add_variables(ssn, properties_map):

    for variable, properties in properties_map.items():
        pass


def set_dimensions(ssn, dimension_map):
    """

    Args:
        ssn: db.session
        project_id: project id
        dimension_map: dict with keys=dimension level,
        values - list of dimensions

    """
    for level_name, dimensions in dimension_map.items():
        for dimension in dimensions:
            new_dimension = Dimension()
            new_dimension.name = dimension
            # depth?
            new_level = DimensionLevel()
            new_level.name = level_name
            new_dimension.levels.append(new_level)
        ssn.add(new_level)


def add_timescales(ssn, project_id, time_periods_map):
    for period_name, time_scales in time_periods_map:
        for time_scale in time_scales:
            new_time_scale = Timescale(name=time_scale, project_id=project_id)
            new_period = TimePeriod(name=period_name)
            new_period.timescale.append(new_time_scale)
            ssn.add(new_period)


def __check_dupl_client(ssn, name, code):
    clients = ssn.query(Client)\
        .filter(or_(Client.code == code,
                    Client.name == name)).all()
    if len(clients) > 0:
        if clients[0].code == code and clients[0].name == name:
            raise ex.AlreadyExistsError('Client', 'code', code)
        elif clients[0].code == code:
            raise ex.AlreadyExistsError('Client', 'code', code)
        else:
            raise ex.AlreadyExistsError('Client', 'name', name)


def __check_none_obj(**kwargs):
    ''' Args:
    -- object=object
    '''
    for key, value in kwargs.items():
        if value is None:
            raise ex.EmptyInputsError(key)

"""

# endregion Clients



def add_user(db, email, password, client):

    #self.__check_none_obj(client=client)
    #existed_user = self.get_user(email=email)

    #if existed_user is not None:
    #    class_name = existed_user.__class__.__name__
    #    raise ex.AlreadyExistsError(class_name, 'email', email)
    new_user = User(email=email, password=password)
    client.users.append(new_user)
    return new_user


def get_user(db, **kwargs):
    '''Possible keys:
    -- id
    -- email
    '''
    if 'id' in kwargs:
        id = int(kwargs['id'])
        return db.query(User).get(id)
    if 'email' in kwargs:
        email = kwargs['email']
        return db.query(User) \
            .filter(User.email == email).one_or_none()
    raise ex.WrongArgsError('get_user')




class WarehouseCommon():
    '''
    Class for metadata management. 
    '''
    def __init__(self, db_connector):
        self.db = db_connector



    #region Users

        
    def delete_user(self, id):
        existed_user = self.get_user(id=int(id))
        if existed_user is None:
            raise ex.NotExistsError('User', 'id', id)
        self.db.session.delete(existed_user)
        self.db.session.commit()

    def update_user(self, id, new_email, new_password):
        need_commit = False
        existed_user = self.get_user(id=int(id))
        if existed_user is None:
            raise ex.NotExistsError('User', 'id', id)
        if existed_user.password != new_password:
            existed_user.password = new_password
            need_commit = True
        if existed_user.email !=new_email:
            dupl_user = self.get_user(email=new_email)
            if dupl_user is not None:
                class_name = dupl_user.__class__.__name__
                raise ex.AlreadyExistsError(class_name, 'email', email)
            existed_user.email = new_email
            need_commit = True
        if need_commit:
            self.db.session.commit()
        return existed_user

    def get_user(self, **kwargs):
        '''Possible keys:
        -- id
        -- email
        '''
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(User).get(id)
        if 'email' in kwargs:
            email = kwargs['email']
            return self.db.session.query(User)\
                .filter(User.email == email).one_or_none()
        raise ex.WrongArgsError('get_user')
    #endregion Users

    #region Projects
    def get_project(self, **kwargs):
        '''Possible keys:
        -- id
        -- code
        '''
        if 'code' in kwargs:
            code = kwargs['code']
            return self.db.session.query(Project)\
                .filter(Project.code == code).one_or_none()
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(Project).get(id)
        raise ex.WrongArgsError('get_project')

    def add_project(self, name, description, code, client):
        self.__check_none_obj(client=client)
        existed_projects = self.get_project(code=code)
        if existed_projects is not None:
            raise ex.AlreadyExistsError('Project', 'code', code)
        new_project = Project()
        new_project.name = name
        new_project.description = description
        new_project.code = code
        client.projects.append(new_project)
        self.db.session.commit()
        return new_project

    def delete_project(self, id):
        existed_project = self.get_project(id=int(id))
        if existed_project is None:
            raise ex.NotExistsError('Project', 'id', id)
        self.db.session.delete(existed_project)
        self.db.session.commit()

    def update_project(self, id, new_name, new_desc, new_code):
        curr_proj = self.get_project(id=int(id))
        if curr_proj is None:
            raise ex.NotExistsError('Project', 'id', id)
        if curr_proj.code != new_code or curr_proj.name != new_name:
            client_id = curr_proj.client_id
            duplicates = self.db.session.query(Project)\
                .filter(or_(Project.code == new_code,
                            and_(Project.name == new_name, 
                                 Project.client_id == client_id))).all()
            if len(duplicates) > 0:
                dupl_proj = duplicates[0]
                class_name = dupl_proj.__class__.__name__
                if dupl_proj.code == new_code:
                    raise ex.AlreadyExistsError(class_name, 'code', new_code)
                else:
                    raise ex.AlreadyExistsError(class_name, 'name', new_name)
            curr_proj.code = new_code
            curr_proj.name = new_name
            curr_proj.description = new_desc
            self.db.session.commit()
            return curr_proj
        elif curr_proj.description != new_desc:
            curr_proj.description = new_desc
            self.db.session.commit()
            return curr_proj
        else:
            class_name = curr_proj.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_project')
    #endregion Projects

    #region Clients
    def add_client(self, name, code):
        #search for duplicate by name or code
        self.__check_dupl_client(name, code)
        new_client = Client()
        new_client.name = name
        new_client.code = code
        self.db.session.add(new_client)
        self.db.session.commit()
        return new_client

    def delete_client(self, id):
        existed_client = self.get_client(id=int(id))
        if existed_client is None:
            raise ex.NotExistsError('Client', 'id', id)
        self.db.session.delete(existed_client)
        self.db.session.commit()

    def update_client(self, id, new_name, new_code):
        existed_client = self.get_client(id=int(id))
        if existed_client is None:
            raise ex.NotExistsError('Client', 'id', id)
        if existed_client.name != new_name or existed_client.code != new_code:
            duplicates = self.db.session.query(Client)\
                .filter(or_(Client.name == new_name,
                            Client.code == new_code)).all()
            if len(duplicates) > 0:
                dupl_proj = duplicates[0]
                class_name = dupl_client.__class__.__name__
                if dupl_proj.name == new_name:
                    raise ex.AlreadyExistsError(class_name, 'name', new_name)
                elif dupl_proj.code == new_code:
                    raise ex.AlreadyExistsError(class_name, 'code', new_code)
            existed_client.name = new_name
            existed_client.code = new_code
            self.db.session.commit()
            return existed_client
        else:
            class_name = existed_client.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_client')

    def get_client(self, **kwargs):
        '''Possible keys:
        -- id
        '''
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(Client).get(id)
        #if 'code' in kwargs:
        #    client_code = kwargs['code']
        #    return self.db.session.query(Client)\
        #        .filter(Client.code == client_code).one_or_none()
        return None

    def __check_dupl_client(self, name, code):
        clients = self.db.session.query(Client)\
                        .filter(or_(Client.code == code,\
                        Client.name == name)).all()
        if len(clients) > 0:
            if clients[0].code == code and clients[0].name == name:
                raise ex.AlreadyExistsError('Client', 'code', code)
            elif clients[0].code == code:
                raise ex.AlreadyExistsError('Client', 'code', code)
            else:
                raise ex.AlreadyExistsError('Client', 'name', name)
    #endregion Clients

    #region Roles
    def add_role(self, role_name, client):
        self.__check_none_obj(client=client)
        existed_role = self.get_role(name=role_name, client_id=client.id)
        if existed_role is not None:
            raise ex.AlreadyExistsError(existed_role.__class__.__name__,\
                'name, client_id', role_name + ', ' + str(client.id))
        new_role = Role()
        new_role.name = role_name
        client.roles.append(new_role)
        self.db.session.commit()
        return new_role

    def update_role(self, id, new_name):
        existed_role = self.get_role(id=int(id))
        if existed_role is None:
            raise ex.NotExistsError('Role', 'id', str(id))
        if existed_role.name != new_name:
            dupl_role = self.db.session.query(Role)\
                .filter(Role.name == new_name, 
                        Role.client_id == existed_role.client_id)\
                            .one_or_none()
            if dupl_role is not None:
                class_name = dupl_role.__class__.__name__
                raise ex.AlreadyExistsError(class_name, 'name', new_name)
            existed_role.name = new_name
            self.db.session.commit()
            return existed_role
        else:
            class_name = existed_role.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_role')

    def delete_role(self, id):
        existed_role = self.get_role(id=int(id))
        if existed_role is None:
            raise ex.NotExistsError('Role', 'id', str(id))
        self.db.session.delete(existed_role)
        self.db.session.commit()

    def get_role(self, **kwargs):
        '''Possible keys:
        -- id
        -- name, client_id
        '''
        if 'name' in kwargs and 'client_id' in kwargs:
            name = kwargs['name']
            client_id = int(kwargs['client_id'])
            return self.db.session.query(Role)\
                .filter(Role.name == name, Role.client_id == client_id)\
                .one_or_none()
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(Role).get(id)
        raise ex.WrongArgsError('get_role')
    #endregion Roles

    #region Timescales
    def add_timescale(self, name, project):
        self.__check_none_obj(project=project)
        existed_ts = self.get_timescale(name=name, project_id=project.id)
        if existed_ts is not None:
            class_name = existed_ts.__class__.__name__
            raise ex.AlreadyExistsError(class_name, 'name', name)
        new_ts = Timescale()
        new_ts.name = name
        project.timescales.append(new_ts)
        self.db.session.commit()
        return new_ts

    def get_timescale(self, **kwargs):
        '''Possible keys:
        -- id
        -- name, project_id
        '''
        if 'name' in kwargs and 'project_id' in kwargs:
            name = kwargs['name']
            project_id = int(kwargs['project_id'])
            return self.db.session.query(Timescale)\
                .filter(Timescale.name == name,\
                Timescale.project_id == project_id).one_or_none()
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(Timescale).get(id)
        raise ex.WrongArgsError('get_timescale')

    def delete_timescale(self, id):
        existed_ts = self.get_timescale(id=int(id))
        if existed_ts is None:
            raise ex.NotExistsError('Timescale', 'id', str(id))
        self.db.session.delete(existed_ts)
        self.db.session.commit()

    def update_timescale(self, id, new_name):
        existed_ts = self.get_timescale(id=int(id))
        if existed_ts is None:
            raise ex.NotExistsError('Timescale', 'id', str(id))
        if existed_ts.name != new_name:
            dupl_ts = self.db.session.query(Timescale)\
                .filter(Timescale.name == new_name,\
                Timescale.project_id == existed_ts.project_id).one_or_none()
            if dupl_ts is not None:
                class_name = dupl_ts.__class__.__name__
                raise ex.AlreadyExistsError(class_name, 'name', new_name)
            existed_ts.name = new_name
            self.db.session.commit()
            return existed_ts
        else:
            class_name = existed_project.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_timescale')
    #endregion Timescales

    #region Features
    def add_feature(self, tool, name, permissions):
        self.__check_none_obj(tool=tool)
        if not isinstance(permissions, list):
            raise ex.EmptyInputsError('FeaturePermission')
        existed_feature = self.get_feature(tool_id=tool.id, name=name)
        if existed_feature is not None:
            class_name = existed_feature.__class__.__name__
            raise ex.AlreadyExistsError(class_name, 'name', name)
        new_feature = Feature()
        new_feature.name = name
        tool.features.append(new_feature)
        if len(permissions) > 0:
            for perm_name in permissions:
                new_perm = FeaturePermission()
                new_perm.name = perm_name
                new_feature.permissions.append(new_perm)
        else:
            raise ex.EmptyInputsError('FeaturePermission') 
        self.db.session.commit()
        return new_feature

    def get_feature(self, **kwargs):
        '''Possible keys:
        -- id
        -- name, tool_id
        '''
        for key, value in kwargs.items():
            if key == 'name':
                if 'tool_id' not in kwargs:
                    raise ex.WrongArgsError('get_feature')
                tool_id = int(kwargs['tool_id'])
                return self.db.session.query(Feature)\
                .filter(Feature.name == value,
                        Feature.tool_id == tool_id).one_or_none()
            if key == 'id':
                return self.db.session.query(Feature).get(int(value))
        raise ex.WrongArgsError('get_feature')

    def delete_feature(self, id):
        existed_feature = self.get_feature(id=id)
        if existed_feature is None:
            raise ex.NotExistsError('Feature', 'id', id)
        self.db.session.delete(existed_feature)
        self.db.session.commit()

    def update_feature(self, id, new_name, permissions):
        need_commit = False
        if not isinstance(permissions, list):
            raise ex.EmptyInputsError('FeaturePermission')
        if len(permissions) == 0:
            raise ex.EmptyInputsError('FeaturePermission')
        existed_feature = self.get_feature(id=id)
        if existed_feature is None:
            raise ex.NotExistsError('Feature', 'id', id)
        if existed_feature.name != new_name:
            dupl_feature = self.get_feature(tool_id=existed_feature.tool_id, 
                                            name=new_name)
            if dupl_feature is not None:
                raise ex.AlreadyExistsError('Feature', 'name', new_name)
            existed_feature.name = new_name
            need_commit = True
        existed_perms = self.db.session.query(FeaturePermission)\
                .filter(FeaturePermission.feature_id == existed_feature.id)\
                .all()
        if len(existed_perms) == 0:
            raise ex.NotExistsError('FeaturePermission','feature_id',
                                    existed_feature.id)
        #items to delete
        ids_to_delete = []
        for item in existed_perms:
            is_not_found = True
            for new_name in permissions:
                if item.name == new_name:
                    is_not_found = False
                    break
            if is_not_found:
                ids_to_delete.append(item.id)
        #names to add
        perms_to_add = []
        for new_name in permissions:
            is_not_found = True
            for item in existed_perms:
                if item.name == new_name:
                    is_not_found = False
                    break
            if is_not_found:
                new_perm = FeaturePermission()
                new_perm.name = new_name
                perms_to_add.append(new_perm)
        #apply changes
        if len(ids_to_delete) > 0:
            objects_to_delete = self.db.session.query(FeaturePermission)\
                .filter(FeaturePermission.id.in_(ids_to_delete))
            objects_to_delete.delete(synchronize_session=False)
            need_commit = True
        if len(perms_to_add) > 0:
            existed_feature.permissions.extend(perms_to_add)
            need_commit = True
        if need_commit:
            self.db.session.commit()
            return existed_feature
        else:
            class_name = existed_feature.__class__.__name__
            raise ex.NoCnahgesError(class_name, 'update_feature')
    #endregion Features
    
    #region Tool
    def add_tool(self, name):
        dupl_tool = self.get_tool(name=name)
        if dupl_tool is not None:
            class_name = dupl_tool.__class__.__name__
            raise ex.AlreadyExistsError(class_name, 'name', name)
        new_tool = Tool()
        new_tool.name = name
        self.db.session.add(new_tool)
        self.db.session.commit()
        return new_tool
        
    def get_tool(self, **kwargs):
        '''Possible keys:
        -- id
        -- name
        '''
        if 'id' in kwargs:
            id = int(kwargs['id'])
            return self.db.session.query(Tool).get(id)
        if 'name' in kwargs:
            name = kwargs['name']
            return self.db.session.query(Tool)\
                .filter(Tool.name == name).one_or_none()
        raise ex.WrongArgsError('get_tool')

    def update_tool(self, id, new_name):
        curr_tool = self.get_tool(id=id)
        if curr_tool is None:
            raise ex.NotExistsError('Tool', 'id', id)
        dupl_tool = self.get_tool(name=new_name)
        if dupl_tool is not None:
            class_name = dupl_tool.__class__.__name__
            raise ex.AlreadyExistsError(class_name, 'name', name)
        curr_tool.name = new_name
        self.db.session.commit()
        return curr_tool

    def delete_tool(self, id):
        curr_tool = self.get_tool(id=id)
        if curr_tool is None:
            raise ex.NotExistsError('Tool', 'id', id)
        self.db.session.delete(curr_tool)
        self.db.session.commit()

    
    #endregion Tool

#Common functions
    def __check_none_obj(self, **kwargs):
        ''' Args:
        -- object=object
        '''
        for key, value in kwargs.items():
            if value is None:
                raise ex.EmptyInputsError(key)
"""