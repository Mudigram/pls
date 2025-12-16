from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.db.models.production_log import ProductionLog
from app.schemas.production_log import ProductionLogUpdate


def create_production_log(db: Session, data):
    # 1. Prevent duplicate active logs for the same moment
    existing_log = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.well_id == data.well_id,
            ProductionLog.log_date == data.log_date,
            ProductionLog.log_time == data.log_time,
            ProductionLog.is_active == True
        )
        .first()
    )

    if existing_log:
        raise HTTPException(
            status_code=400,
            detail="An active production log already exists for this well at the specified date and time"
        )

    # 2. Create first revision
    new_log = ProductionLog(
        well_id=data.well_id,
        log_date=data.log_date,
        log_time=data.log_time,
        oil_bbl=data.oil_bbl,
        gas_mscf=data.gas_mscf,
        water_bbl=data.water_bbl,
        remarks=data.remarks,
        revision_count=1,
        is_active=True
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


def revise_production_log(
    db: Session,
    log_id: int,
    update: ProductionLogUpdate
):
    # 1. Fetch active log
    old_log = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.id == log_id,
            ProductionLog.is_active == True
        )
        .first()
    )

    if not old_log:
        raise HTTPException(
            status_code=404,
            detail="Active production log not found"
        )

    # 2. Retire old log
    old_log.is_active = False

    # 3. Create revised log
    new_log = ProductionLog(
        well_id=old_log.well_id,
        log_date=old_log.log_date,
        log_time=old_log.log_time,
        oil_bbl=update.oil_bbl if update.oil_bbl is not None else old_log.oil_bbl,
        gas_mscf=update.gas_mscf if update.gas_mscf is not None else old_log.gas_mscf,
        water_bbl=update.water_bbl if update.water_bbl is not None else old_log.water_bbl,
        remarks=update.remarks if update.remarks is not None else old_log.remarks,
        revision_count=old_log.revision_count + 1,
        is_active=True
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log