from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship, backref
from passlib.hash import bcrypt
from iap.common.repository.db.meta import Base
from .scenarios import user_scenario_table
import datetime

project_tool_tbl = Table("project_tool", Base.metadata,
                                Column("projects_id", String, ForeignKey("projects.id"), primary_key=True),
                                Column("tools_id", String, ForeignKey("tool.id"), primary_key=True)
                          )

class Project(Base):
    __tablename__ = "projects"
    id = Column(String , primary_key=True)
    name = Column(String(length=255))
    description = Column(String())
    tools = relationship("Tool", secondary=project_tool_tbl, back_populates="projects")


class Tool(Base):
    __tablename__ = "tool"

    id = Column(String, primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))

    project_id = Column(Integer, ForeignKey('projects.id'))

    projects = relationship("Project", secondary=project_tool_tbl, back_populates="tools")

    roles = relationship("Role", backref="tool")
    # Maybe configure join  via...
    features = relationship("Feature", backref="tool")
    user_groups = relationship("UserGroup", backref="tool")

"""
class Tool(Base):
    __tablename__ = 'tool'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))



    roles = relationship("Role", backref="tool")
    # Maybe configure join  via...
    features = relationship("Feature", backref="tool")
    user_groups = relationship("UserGroup", backref="tool")
"""

user_role_tbl = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

user_ugroup_tbl = Table(
    'user_ugroup', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('user_groups.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(length=255))
    password = Column(String(length=255))

    profile = relationship('UserProfile', uselist=False,
                           back_populates='user')
    roles = relationship('Role', secondary=user_role_tbl,
                         back_populates='users')
    groups = relationship('UserGroup', secondary=user_ugroup_tbl,
                          back_populates='users')

    scenarios = relationship(
        "Scenario",
        secondary=user_scenario_table,
        back_populates="users")

    perms = relationship("Permission", back_populates="user")

    foreacst_perm_values = relationship("FrcastPermValue")

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)

    def check_password(self, password):
        print(bcrypt.verify(password, self.password))
        return bcrypt.verify(password, self.password)

role_features_tbl = Table(
    'role_feature', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('feature_id', Integer, ForeignKey('features.id'))
)


class DataPermission(Base):
    __tablename__ = "data_permissions"
    id = Column(Integer, primary_key=True)
    out_path = Column(String(length=255))
    in_path = Column(String(length=255))
    project = Column(String(length=255))
    mask = Column(Integer)
    perm_id = Column(Integer, ForeignKey("permissions.id"))
    perm = relationship('Permission', back_populates='data_perms')


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    data_perms = relationship('DataPermission', back_populates="perm")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship('User', back_populates='perms')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    tool_id = Column(Integer, ForeignKey('tool.id'))

    # there is link for tool

    # TODO Clean
    users = relationship('User', secondary=user_role_tbl,
                         back_populates='roles')
    features = relationship('Feature', secondary=role_features_tbl,
                            back_populates='roles')


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))

    tool_id = Column(Integer, ForeignKey('tool.id'))

    # there is link for tool

    # TODO Clean
    roles = relationship('Role', secondary=role_features_tbl,
                         back_populates='features')



class UserProfile(Base):
    __tablename__ = 'users_profiles'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    user = relationship('User', back_populates='profile')


#Permission for Data Access
group_perm_ass_tbl = Table('group_perm_ass', Base.metadata,
    Column('group_id', Integer, ForeignKey('user_groups.id')),
    Column('data_perm_id', Integer, ForeignKey('data_permission_access.id'))
)


class UserGroup(Base):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    tool_id = Column(Integer, ForeignKey('tool.id'))

    #  there is variable-link to tool

    users = relationship('User', secondary=user_ugroup_tbl,
                         back_populates='groups')
    data_perm = relationship("DataPermissionAccess", secondary=group_perm_ass_tbl,
                            back_populates="groups")


class DataPermissionAccess(Base):
    __tablename__ = "data_permission_access"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))#description
    value = Column(String(length=255))
    groups = relationship("UserGroup",secondary=group_perm_ass_tbl, back_populates="data_perm")

# region Models For User's Permissions to ForecastTool

frcast_perm_node_hier_tbl = Table("forecast_perm_node_hier", Base.metadata,
                                  Column("node_id", Integer,
                                         ForeignKey("forecast_perm_node.id"),
                                         primary_key=True),
                                  Column("parent_node_id", Integer,
                                         ForeignKey("forecast_perm_node.id"),
                                         primary_key=True)
                                  )


class FrcastPermNode(Base):
    __tablename__ = 'forecast_perm_node'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    node_type = Column(String(length=16))
    perm_values = relationship("FrcastPermValue", back_populates='perm_node')

    children = relationship("FrcastPermNode",
                            secondary=frcast_perm_node_hier_tbl,
                            primaryjoin=id ==
                                    frcast_perm_node_hier_tbl.c.parent_node_id,
                            secondaryjoin=id ==
                                          frcast_perm_node_hier_tbl.c.node_id,
                            backref="node_id")

    parents = relationship("FrcastPermNode",
                           secondary=frcast_perm_node_hier_tbl,
                           primaryjoin=id ==
                                       frcast_perm_node_hier_tbl.c.node_id,
                           secondaryjoin=id ==
                                     frcast_perm_node_hier_tbl.c.parent_node_id,
                           backref="parent_node_id")


class FrcastPermValue(Base):
    __tablename__ = 'forecast_perm_value'
    id = Column(Integer, primary_key=True)
    perm_node_id = Column(Integer, ForeignKey('forecast_perm_node.id'))
    value = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    perm_node = relationship("FrcastPermNode", back_populates='perm_values')

# endregion

PERMS_MODELS_MAP = {
    'forecast': {'node': FrcastPermNode, 'value': FrcastPermValue},
    'ppt': {'node': None, 'value': None},
    'mmm': {'node': None, 'value': None}
}


# class UserDataAccess(Base):
#     __tablename__ = 'user_data_access'
#
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     feature_id = Column(Integer,
#                         ForeignKey('features.id'),
#                         primary_key=True)
#     variable_id = Column(Integer, ForeignKey('variable.id'), primary_key=True)
#     decline_flag = Column(Boolean(create_constraint=True, name='validator'),
#                           default=False)
#
#
# class UserGroupDataAccess(Base):
#     __tablename__ = 'user_group_data_access'
#
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     feature_id = Column(Integer,
#                         ForeignKey('features.id'),
#                         primary_key=True)
#     variable_id = Column(Integer, ForeignKey('variable.id'), primary_key=True)
#     decline_flag = Column(Boolean(create_constraint=True, name='validator'),
#                           default=False)






