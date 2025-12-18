from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.db.models.production_log import ProductionLog
from app.schemas.production_log import ProductionLogUpdate
from datetime import date, time


def create_production_log(
    db: Session,
    well_id: int,
    production_date: date,
    oil_bbl: float,
    gas_mscf: float,
    water_bbl: float,
    remarks: str | None = None,
):
    existing_log = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.well_id == well_id,
            ProductionLog.production_date == production_date,
            ProductionLog.is_active == True
        )
        .first()
    )

    if existing_log:
        raise ValueError("Active production log already exists")

    new_log = ProductionLog(
        well_id=well_id,
        production_date=production_date,
        oil_bbl=oil_bbl,
        gas_mscf=gas_mscf,
        water_bbl=water_bbl,
        remarks=remarks,
        revision_count=0,
        is_active=True,
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


# def update_production_log(
#     db: Session,
#     log_id: int,
#     oil_bbl: float | None = None,
#     gas_mscf: float | None = None,
#     water_bbl: float | None = None,
# ):
#     log = db.query(ProductionLog).filter(
#         ProductionLog.id == log_id,
#         ProductionLog.is_active == True
#     ).first()

#     if not log:
#         raise ValueError("Production log not found")

#     if oil_bbl is not None:
#         log.oil_bbl = oil_bbl
#     if gas_mscf is not None:
#         log.gas_mscf = gas_mscf
#     if water_bbl is not None:
#         log.water_bbl = water_bbl

#     log.revision_count += 1
#     log.updated_at = datetime.utcnow()

#     db.commit()
#     db.refresh(log)
#     return log

def revise_production_log(
    db: Session,
    log_id: int ,
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