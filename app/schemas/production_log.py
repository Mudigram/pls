from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional

class ProductionLogBase(BaseModel):
    well_id: int = Field(..., gt=0)
    log_date: date
    log_time: time

    oil_bbl: float = Field(..., ge=0)
    gas_mscf: float = Field(..., ge=0)
    water_bbl: float = Field(..., ge=0)

    remarks: Optional[str] = None


class ProductionLogCreate(ProductionLogBase):
    pass

class ProductionLogResponse(ProductionLogBase):
    id: int
    revision_count: int
    is_active: bool

    class Config:
        orm_mode = True


class ProductionLogUpdate(BaseModel):
    oil_bbl: Optional[float] = Field(None, ge=0)
    gas_mscf: Optional[float] = Field(None, ge=0)
    water_bbl: Optional[float] = Field(None, ge=0)
    remarks: Optional[str] = None
    is_active: bool
