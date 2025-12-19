from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.deps import get_db
from app.services.reporting_services import (
    get_daily_production_totals,
    get_monthly_production_totals,
)
from app.services.reporting_services import get_well_production_summary
from app.schemas.reports import WellProductionSummary, MonthlyProductionSummary

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get("/daily/{well_id}/{production_date}")
def get_daily_production_totals(
    well_id: int,
    production_date: date,
    db: Session = Depends(get_db),
):
    return get_daily_production_totals(db, well_id, production_date)

@router.get("/wells/{well_id}/monthly")
def monthly_production_report(
    well_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
):
    return get_monthly_production_totals(
        db=db,
        well_id=well_id,
        year=year,
        month=month,
    )

@router.get("/wells/{well_id}/daily-water-cut/{target_date}")
def daily_water_cut_report(
    well_id: int,
    target_date: date,
    db: Session = Depends(get_db),
):
    return get_daily_water_cut(db, well_id, target_date)


@router.get(
    "/wells/{well_id}/summary",
    response_model=WellProductionSummary
)
def well_production_summary(
    well_id: int,
    start: date,
    end: date,
    db: Session = Depends(get_db)
):
    summary = get_well_production_summary(
        db=db,
        well_id=well_id,
        start_date=start,
        end_date=end
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="No production data found for this well in the given period"
        )

    return summary

@router.get(
    "/wells/{well_id}/monthly-summary/{year}/{month}",
    response_model=MonthlyProductionSummary
)
def monthly_production_summary(
    well_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    summary = get_monthly_production_summary(
        db=db,
        well_id=well_id,
        year=year,
        month=month
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="No production data found for this well in the given period"
        )

    return summary

@router.get(
    "/wells/{well_id}/water-cut-trend/{days}")
def water_cut_trend(
    well_id: int,
    days: int = 7,
    db: Session = Depends(get_db)
):
    data = get_water_cut_trend(db, well_id, days)

    return {
        "well_id": well_id,
        "window_days": days,
        "data": data
    }