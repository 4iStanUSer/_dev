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
from ..db.meta import Base

class PredefScenario(Base):
    __tablename__ = "predef_sceanrio"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))
    entity  = Column(String(length=255))
    timeline = Column(String(length=255))
    variable = Column(String(length=255))
    timestamp = Column(String(length=255))
    value = Column(String(length=255))