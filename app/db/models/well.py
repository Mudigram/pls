from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    well_name = Column(String, nullable=False)
    status = Column(String, default="active")
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    field = relationship("Field", backref="wells")
    description = Column(String, nullable=True)