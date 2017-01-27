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


class Scenario(Base):

    __tablename__ = 'scenarios'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('scenarios.id'), nullable=True)

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

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="scenarios")

    children = relationship("Scenario",  remote_side=[id])