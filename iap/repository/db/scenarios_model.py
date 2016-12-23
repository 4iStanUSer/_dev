from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Interval,
    DateTime
)
from sqlalchemy.orm import relationship, backref
from .models_access import User
from passlib.hash import bcrypt
from .meta import Base


class Scenario(Base):
    __tablename__ = 'scenario'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('scenario.id'))

    name = Column(String(length=255))
    description = Column(String(length=255))
    date_of_lat_modification = Column(DateTime)

    status = Column(String(length=255))
    shared = Column(String(length=255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    geographies = Column(String(length=255))
    products = Column(String(length=255))
    channel = Column(String(length=255))

    #author = relationship("User", backref="scenario")

    children = relationship("Scenario",  remote_side=[id])



