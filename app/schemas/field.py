from pydantic import BaseModel, Field
from typing import Optional


class FieldBase(BaseModel):
    name: str = Field(..., min_length=2)
    location: Optional[str] = None
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class FieldCreate(FieldBase):
    pass

class FieldResponse(FieldBase):
    id: int

    class Config:
        orm_mode = True

class FieldUpdate(FieldBase):
    id: int

    class Config:
        orm_mode = True