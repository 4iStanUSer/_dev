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


point_coordinates = Table(
    'point_coordinates',
    Base.metadata,
    Column('point_id', Integer, ForeignKey('points.id')),
    Column('hierarchy_id', Integer, ForeignKey('hierarchies.id'))
)


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


role_feature_permissions = Table(
    'role_feature_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('feature_permission_id', Integer,
           ForeignKey('feature_permissions.id'))
)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    code = Column(String(length=255))
    name = Column(String(length=255))
    users = relationship('User', back_populates='client')
    roles = relationship('Role', back_populates='client')
    projects = relationship('Project', back_populates='client')


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    code = Column(String(length=255))
    name = Column(String(length=255))
    description = Column(String(length=255))
    client = relationship('Client', back_populates='projects')
    timescales = relationship('Timescale', back_populates='project')
    dimensions = relationship('Dimension', back_populates='project')
    num_vars = relationship('NumericalVariable', back_populates='project')
    cat_vars = relationship('CategoricalVariable', back_populates='project')
    coefficients = relationship('Coefficient', back_populates='project')


class Timescale(Base):
    __tablename__ = 'timescales'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(length=255))
    project = relationship('Project', back_populates='timescales')
    time_periods = relationship('TimePeriod', back_populates='timescale')


class TimePeriod(Base):
    __tablename__ = 'time_periods'
    id = Column(Integer, primary_key=True)
    timescale_id = Column(Integer, ForeignKey('timescales.id'))
    parent_id = Column(Integer, ForeignKey('time_periods.id'))
    name = Column(String(length=255))
    timescale = relationship('Timescale', back_populates='time_periods')
    children = relationship('TimePeriod', 
                            backref=backref('parent', remote_side=[id]))


class Dimension(Base):
    __tablename__ = 'dimensions'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(length=255))
    project = relationship('Project', back_populates='dimensions')
    levels = relationship('DimensionLevel', back_populates='dimension')
    hierarchy_items = relationship('Hierarchy', back_populates='dimension')


class DimensionLevel(Base):
    __tablename__ = 'dimension_levels'
    id = Column(Integer, primary_key=True)
    dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    name = Column(String(length=255))
    depth = Column(Integer)
    dimension = relationship('Dimension', back_populates='levels')


class Hierarchy(Base):
    __tablename__ = 'hierarchies'
    id = Column(Integer, primary_key=True)
    dimension_id = Column(Integer, ForeignKey('dimensions.id'))
    level_id = Column(Integer, ForeignKey('dimension_levels.id'))
    parent_id = Column(Integer, ForeignKey('hierarchies.id'))
    depth = Column(Integer)
    name = Column(String(length=255))
    dimension = relationship('Dimension', back_populates='hierarchy_items')
    children = relationship('Hierarchy', 
                            backref=backref('parent', remote_side=[id]))


class VariableType(Base):
    __tablename__ = 'variable_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))


class NumericalVariable(Base):
    __tablename__ = 'numerical_variables'
    id = Column(Integer, primary_key=True)
    variable_type_id = Column(Integer, ForeignKey('variable_types.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(length=255))
    metric = Column(String(length=255))
    metric_multiplier = Column(Integer)
    type = relationship('VariableType')
    project = relationship('Project', back_populates='num_vars')


class CategoricalVariable(Base):
    __tablename__ = 'categorical_variables'
    id = Column(Integer, primary_key=True)
    variable_type_id = Column(Integer, ForeignKey('variable_types.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(length=255))
    possible_values = relationship('PossibleValues')
    type = relationship('VariableType')
    project = relationship('Project', back_populates='cat_vars')


class PossibleValues(Base):
    __tablename__ = 'possible_values'
    id = Column(Integer, primary_key=True)
    variable_id = Column(Integer, ForeignKey('categorical_variables.id'))
    name = Column(String(length=255))


class Point(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    coordinates = relationship('Hierarchy', secondary=point_coordinates)
    num_values = relationship('NumVarValue')
    cat_values = relationship('CatVarValue')
    coefficient_values = relationship('CoefficientValue')


class NumVarValue(Base):
    __tablename__ = 'num_var_values'
    point_id = Column(Integer, ForeignKey('points.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('numerical_variables.id'),
                         primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    value = Column(Float)
    point = relationship('Point', back_populates='num_values')
    variable = relationship('NumericalVariable')
    time_period = relationship('TimePeriod')


class CatVarValue(Base):
    __tablename__ = 'cat_var_values'
    point_id = Column(Integer, ForeignKey('points.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('categorical_variables.id'),
                         primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    value_id = Column(Integer, ForeignKey('possible_values.id'))
    point = relationship('Point', back_populates='cat_values')
    variable = relationship('CategoricalVariable')
    value = relationship('PossibleValues')
    time_period = relationship('TimePeriod')


class Coefficient(Base):
    __tablename__ = 'coefficients'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(length=255))
    timeline_flag = Column(Boolean(create_constraint=True, name='validator'),
                           default=False)
    project = relationship('Project', back_populates='coefficients')


class CoefficientValue(Base):
    __tablename__ = 'coefficient_timeseries'
    coefficient_id = Column(Integer, ForeignKey('coefficients.id'),
                            primary_key=True)
    point_id = Column(Integer, ForeignKey('points.id'), primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    value = Column(Float)
    coefficient = relationship('Coefficient')
    time_period = relationship('TimePeriod')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    email = Column(String(length=255))
    password = Column(String(length=255))
    client = relationship('Client', back_populates='users')
    profile = relationship('UserProfile', uselist=False, 
                           back_populates='user')
    roles = relationship('Role', secondary=user_roles,
                         back_populates='users')


class UserProfile(Base):
    __tablename__ = 'users_profiles'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    user = relationship('User', back_populates='profile')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    name = Column(String(length=255))
    client = relationship('Client', back_populates='roles')
    users = relationship('User', secondary=user_roles,
                         back_populates='roles')
    feature_permissions = relationship('FeaturePermission',
                                       secondary=role_feature_permissions,
                                       back_populates='permitted_roles')


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    tool_id = Column(Integer, ForeignKey('tools.id'))
    permissions = relationship('FeaturePermission')


class FeaturePermission(Base):
    __tablename__ = 'feature_permissions'
    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.id'))
    name = Column(String(length=255))
    permitted_roles = relationship('Role',
                                   secondary=role_feature_permissions,
                                   back_populates='feature_permissions')


class Tool(Base):
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    features = relationship('Feature')
