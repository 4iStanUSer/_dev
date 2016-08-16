from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Float,
    Boolean,
)
from sqlalchemy.orm import relationship, backref
from .meta import Base


class Tool(Base):
    __tablename__ = 'tool'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))

    roles = relationship("Role", backref="tool")
    # Maybe configure join  via...
    features = relationship("Feature", backref="tool")


user_role_tbl = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
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


role_features_tbl = Table(
    'role_feature', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('feature_id', Integer, ForeignKey('features.id'))
)


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


class UserGroup(Base):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))


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
    node_type = Column(String(length=16))
    perm_values = relationship("FrcastPermValue")

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
    user_id = Column(Integer)

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
