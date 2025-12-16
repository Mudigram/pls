from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models.well import Well
from app.schemas.well import WellCreate, WellResponse

router = APIRouter(prefix="/wells", tags=["Wells"])
@router.post("/", response_model=WellResponse)
def create_well(well: WellCreate, db: Session = Depends(get_db)):
    existing = db.query(Well).filter(Well.well_name == well.well_name,  Well.well_name == well.well_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Well already exists")

    new_well = Well(**well.model_dump())
    db.add(new_well)
    db.commit()
    db.refresh(new_well)

    return new_well
@router.get("/", response_model=list[WellResponse])
def get_wells(db: Session = Depends(get_db)):
    wells = db.query(Well).all()
    return wells

@router.get("/{well_id}", response_model=WellResponse)
def get_well(well_id: int, db: Session = Depends(get_db)):
    well = db.query(Well).filter(Well.id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    return well