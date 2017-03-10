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



user_scenario_table = Table('user_scenarios', Base.metadata,
    Column('scenario_id', Integer, ForeignKey('scenarios.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Scenario(Base):

    __tablename__ = 'scenarios'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('scenarios.id'), nullable=True)

    name = Column(String(length=255), nullable=False)
    description = Column(String(length=255))
    date_of_last_modification = Column(String)

    criteria = Column(String)
    favorite = Column(String(length=255), nullable=True, default="No")

    status = Column(String(length=255), default="Draft")
    shared = Column(String(length=255), nullable=True, default="No")
    start_date = Column(DateTime,  nullable=True)
    end_date = Column(DateTime, nullable=True)

    author = Column(String(length=255))
    users = relationship("User", secondary=user_scenario_table, back_populates="scenarios")

    children = relationship("Scenario",  remote_side=[id])


