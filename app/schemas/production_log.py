from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from pydantic import model_validator

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

    @model_validator(mode="after")
    def require_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("At least one field must be updated")
        return values

