from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models.production_log import ProductionLog
from app.schemas.production_log import ProductionLogCreate, ProductionLogResponse, ProductionLogUpdate
from app.services.production_log_services import create_production_log, revise_production_log

router = APIRouter(prefix="/production-logs", tags=["Production Logs"])
@router.post("/", response_model=ProductionLogResponse)
def add_production_log(log: ProductionLogCreate, db: Session = Depends(get_db)):
    new_log = create_production_log(db, log)
    return new_log

@router.get("/", response_model=list[ProductionLogResponse])
def get_production_logs(db: Session = Depends(get_db)):
    logs = db.query(ProductionLog).filter(ProductionLog.is_active == True).all()
    return logs

@router.get("/well/{well_id}", response_model=list[ProductionLogResponse])
def get_production_logs_by_well(well_id: int, db: Session = Depends(get_db)):
    logs = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.well_id == well_id,
            ProductionLog.is_active == True
        )
        .order_by(ProductionLog.log_date.asc())
        .all()
    )

    if not logs:
        raise HTTPException(
            status_code=404,
            detail="No production logs found for this well"
        )

    return logs

@router.get("/{log_id}", response_model=ProductionLogResponse)
def get_production_log_by_id(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ProductionLog).filter(
        ProductionLog.id == log_id,
        ProductionLog.is_active == True
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Production log not found")

    return log

@router.patch("/{log_id}", response_model=ProductionLogResponse)
def revise_log(
    log_id: int,
    update: ProductionLogUpdate,
    db: Session = Depends(get_db)
):
    return revise_production_log(db, log_id, update)
