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
from sqlalchemy.orm import relationship
from iap.common.repository.db.meta import Base



user_scenario_table = Table('user_scenario', Base.metadata,
    Column('scenario_id', Integer, ForeignKey('scenario.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Scenario(Base):

    __tablename__ = 'scenario'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('scenario.id'), nullable=True)

    name = Column(String(length=255))
    description = Column(String(length=255))
    date_of_last_modification = Column(String)

    criteria = Column(String)
    #entity_id = Column(Integer, ForeignKey('entity.id'))
    #enity = relationship("Entity", back_populates="scenarios")

    status = Column(String(length=255))
    shared = Column(String(length=255), nullable=True)
    start_date = Column(DateTime,  nullable=True)
    end_date = Column(DateTime, nullable=True)

    author = Column(String(length=255))
    users = relationship("User", secondary=user_scenario_table, back_populates="scenarios")

    children = relationship("Scenario",  remote_side=[id])