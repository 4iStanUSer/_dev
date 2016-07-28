'''
Module contains db models definition.
'''
from flask_login import UserMixin
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean, 
                        MetaData, ForeignKey, Date)
from sqlalchemy.orm import relationship, backref
from .db_connector import Base

point_coordinates = Table('point_coordinates', Base.metadata, 
    Column('point_id', Integer, ForeignKey('point.id')), 
    Column('hierarchy_id', Integer, ForeignKey('hierarchy.id'))
)

user_roles = Table('user_roles', Base.metadata, 
    Column('user_id', Integer, ForeignKey('user.id')), 
    Column('role_id', Integer, ForeignKey('role.id'))
)

role_feature_permissions =\
    Table('role_feature_permissions', Base.metadata, 
          Column('role_id', Integer, ForeignKey('role.id')), 
          Column('feature_permission_id', Integer, 
                 ForeignKey('feature_permission.id'))
)

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))
    projects = relationship('Project', back_populates='client')
    users = relationship('User', back_populates='client')
    roles = relationship('Role', back_populates='client')


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    code = Column(String(255))
    name = Column(String(255))
    description = Column(String)
    client = relationship('Client', back_populates='projects')
    timescales = relationship('Timescale', back_populates='project')
    dimensions = relationship('Dimension', back_populates='project')
    num_vars = relationship('NumericalVariable', back_populates='project')
    cat_vars = relationship('CategoricalVariable', back_populates='project')
    coefficients = relationship('Coefficient', back_populates='project')


class Timescale(Base):
    __tablename__ = 'timescale'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String(255))
    project = relationship('Project', back_populates='timescales')
    time_periods = relationship('TimePeriod', back_populates='timescale')


class TimePeriod(Base):
    __tablename__ = 'time_period'
    id = Column(Integer, primary_key=True)
    timescale_id = Column(Integer, ForeignKey('timescale.id'))
    parent_id = Column(Integer, ForeignKey('time_period.id'))
    name = Column(String(255))
    timescale = relationship('Timescale', back_populates='time_periods')
    children = relationship('TimePeriod', 
                            backref=backref('parent', remote_side=[id]))


class Dimension(Base):
    __tablename__ = 'dimension'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String(255))
    project = relationship('Project', back_populates='dimensions')
    levels = relationship('DimensionLevel', back_populates='dimension')
    hierarchy_items = relationship('Hierarchy', back_populates='dimension')


class DimensionLevel(Base):
    __tablename__ = 'dimension_level'
    id = Column(Integer, primary_key=True)
    dimension_id = Column(Integer, ForeignKey('dimension.id'))
    name = Column(String(255))
    depth = Column(Integer)
    dimension = relationship('Dimension', back_populates='levels')


class Hierarchy(Base):
    __tablename__ = 'hierarchy'
    id = Column(Integer, primary_key=True)
    dimension_id = Column(Integer, ForeignKey('dimension.id'))
    level_id = Column(Integer, ForeignKey('dimension_level.id'))
    parent_id = Column(Integer, ForeignKey('hierarchy.id'))
    depth = Column(Integer)
    name = Column(String(255))
    dimension = relationship('Dimension', back_populates='hierarchy_items')
    children = relationship('Hierarchy', 
                            backref=backref('parent', remote_side=[id]))


class VariableType(Base):
    __tablename__ = 'variable_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class NumericalVariable(Base):
    __tablename__ = 'numerical_variable'
    id = Column(Integer, primary_key=True)
    variable_type_id = Column(Integer, ForeignKey('variable_type.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String(255))
    metric = Column(String(255))
    metric_multiplier = Column(Integer)
    type = relationship('VariableType')
    project = relationship('Project', back_populates='num_vars')


class CategoricalVariable(Base):
    __tablename__ = 'categorical_variable'
    id = Column(Integer, primary_key=True)
    variable_type_id = Column(Integer, ForeignKey('variable_type.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String(255))
    possible_values = relationship('PossibleValues')
    type = relationship('VariableType')
    project = relationship('Project', back_populates='cat_vars')


class PossibleValues(Base):
    __tablename__ = 'possible_values'
    id = Column(Integer, primary_key=True)
    variable_id = Column(Integer, ForeignKey('categorical_variable.id'))
    name = Column(String(255))


class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    coordinates = relationship('Hierarchy', secondary=point_coordinates) 
    num_values = relationship('NumVarValue')
    cat_values = relationship('CatVarValue')
    coefficient_values = relationship('CoefficientValue')


class NumVarValue(Base):
    __tablename__ = 'num_var_value'
    point_id = Column(Integer, ForeignKey('point.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('numerical_variable.id'), 
                         primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_period.id'))
    value = Column(Float)
    point = relationship('Point', back_populates='num_values')
    variable = relationship('NumericalVariable')
    time_period = relationship('TimePeriod')


class CatVarValue(Base):
    __tablename__ = 'cat_var_value'
    point_id = Column(Integer, ForeignKey('point.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('categorical_variable.id'), 
                         primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_period.id'))
    value_id = Column(Integer, ForeignKey('possible_values.id'))
    point = relationship('Point', back_populates='cat_values')
    variable = relationship('CategoricalVariable')
    value = relationship('PossibleValues')
    time_period = relationship('TimePeriod')


class Coefficient(Base):
    __tablename__ = 'coefficient'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String(255))
    timeline_flag = Column(Boolean)
    project = relationship('Project', back_populates='coefficients')


class CoefficientValue(Base):
    __tablename__ = 'coefficient_timeseries'
    coefficient_id = Column(Integer, ForeignKey('coefficient.id'), 
                            primary_key=True)
    point_id = Column(Integer, ForeignKey('point.id'), primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_period.id'))
    value = Column(Float)
    coefficient = relationship('Coefficient')
    time_period = relationship('TimePeriod')


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    email = Column(String(255))
    password = Column(String(255))
    client = relationship('Client', back_populates='users')
    profile = relationship('UserProfile', uselist=False, 
                           back_populates='user')
    roles = relationship('Role', secondary=user_roles, back_populates='users')


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('user.id'))
    first_name = Column(String(255))
    last_name = Column(String(255))
    user = relationship('User', back_populates='profile')


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    name = Column(String(255))
    client = relationship('Client', back_populates='roles')
    users = relationship('User', secondary=user_roles, back_populates='roles')
    feature_permissions = relationship('FeaturePermission', 
                                       secondary=role_feature_permissions,
                                       back_populates='permitted_roles')


class Feature(Base):
    __tablename__ = 'feature'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    tool_id = Column(Integer, ForeignKey('tools.id'))
    permissions = relationship('FeaturePermission')


class FeaturePermission(Base):
    __tablename__ = 'feature_permission'
    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey('feature.id'))
    name = Column(String(255))
    permitted_roles = relationship('Role', secondary=role_feature_permissions,
                                     back_populates='feature_permissions')
    
class Tool(Base):
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    features = relationship('Feature')
    

#TODO
class ContenetPermission(Base):
    __tablename__ = 'content_permission'
    id = Column(Integer, primary_key=True)
