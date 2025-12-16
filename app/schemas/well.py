from pydantic import BaseModel, Field
from typing import Optional


class WellBase(BaseModel):
    field_id: int = Field(..., gt=0)
    well_name: str = Field(..., min_length=2)
    status: Optional[str] = "active"
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    description: Optional[str] = None

class WellCreate(WellBase):
    pass

class WellResponse(WellBase):
    id: int

    class Config:
        orm_mode = True

class WellUpdate(WellBase):
    id: int
    class Config:
        orm_mode = True