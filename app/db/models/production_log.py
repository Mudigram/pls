from sqlalchemy import Column, String, Boolean, Integer, Float, Date, Time, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ProductionLog(Base):
    __tablename__ = "production_logs"

    id = Column(Integer, primary_key=True, index=True)

    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)

    log_date = Column(Date, nullable=False)
    log_time = Column(Time, nullable=False)

    oil_bbl = Column(Float, nullable=False)
    gas_mscf = Column(Float, nullable=False)
    water_bbl = Column(Float, nullable=False)

    remarks = Column(String, nullable=True)

    revision_count = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    well = relationship("Well", backref="production_logs")

    __table_args__ = (
        UniqueConstraint(
            "well_id",
            "log_date",
            "log_time",
            "is_active",
            name="uq_active_production_log_per_time"
        ),
    )
