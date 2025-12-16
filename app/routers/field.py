from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models.field import Field
from app.schemas.field import FieldCreate, FieldResponse

router = APIRouter(prefix="/fields", tags=["Fields"])

@router.post("/", response_model=FieldResponse)
def create_field(field: FieldCreate, db: Session = Depends(get_db)):
    existing = db.query(Field).filter(Field.name == field.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Field already exists")

    new_field = Field(**field.model_dump())
    db.add(new_field)
    db.commit()
    db.refresh(new_field)

    return new_field

@router.get("/", response_model=list[FieldResponse])
def get_fields(db: Session = Depends(get_db)):
    fields = db.query(Field).all()
    return fields