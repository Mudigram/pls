from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, timedelta

from app.db.models.production_log import ProductionLog

WATER_CUT_ALERT_THRESHOLD = 0.6

def get_daily_production_totals(
    db: Session,
    well_id: int,
    production_date: date,
):
    result = (
        db.query(
            func.coalesce(func.sum(ProductionLog.oil_bbl), 0).label("oil_bbl"),
            func.coalesce(func.sum(ProductionLog.gas_mscf), 0).label("gas_mscf"),
            func.coalesce(func.sum(ProductionLog.water_bbl), 0).label("water_bbl"),
        )
        .filter(
            ProductionLog.well_id == well_id,
            ProductionLog.production_date == production_date,
            ProductionLog.is_active == True,
        )
        .one()
    )

    return {
        "well_id": well_id,
        "date": production_date,
        "oil_bbl": result.oil_bbl,
        "gas_mscf": result.gas_mscf,
        "water_bbl": result.water_bbl,
    }

def get_monthly_production_totals(
    db: Session,
    well_id: int,
    year: int,
    month: int,
):
    result = (
        db.query(
            func.coalesce(func.sum(ProductionLog.oil_bbl), 0).label("oil_bbl"),
            func.coalesce(func.sum(ProductionLog.gas_mscf), 0).label("gas_mscf"),
            func.coalesce(func.sum(ProductionLog.water_bbl), 0).label("water_bbl"),
            func.count(func.distinct(ProductionLog.production_date)).label("days"),
        )
        .filter(
            ProductionLog.well_id == well_id,
            extract("year", ProductionLog.production_date) == year,
            extract("month", ProductionLog.production_date) == month,
            ProductionLog.is_active == True,
        )
        .one()
    )

    avg_daily_oil = (
        result.oil_bbl / result.days if result.days > 0 else 0
    )

    return {
        "well_id": well_id,
        "month": f"{year}-{month:02}",
        "total_oil_bbl": result.oil_bbl,
        "total_gas_mscf": result.gas_mscf,
        "total_water_bbl": result.water_bbl,
        "average_daily_oil": round(avg_daily_oil, 2),
    }

def get_daily_water_cut(
    db: Session,
    well_id: int,
    target_date: date
) -> float:
    """
    Calculate daily water cut percentage.
    """

    totals = db.query(
        func.coalesce(func.sum(ProductionLog.oil_bbl), 0).label("oil"),
        func.coalesce(func.sum(ProductionLog.water_bbl), 0).label("water"),
    ).filter(
        ProductionLog.well_id == well_id,
        ProductionLog.production_date == target_date,
        ProductionLog.is_active == True
    ).first()

    oil = totals.oil
    water = totals.water
    total_liquid = oil + water

    if total_liquid == 0:
        return 0.0

    water_cut = (water / total_liquid) * 100
    return round(water_cut, 2)



def get_well_production_summary(
    db: Session,
    well_id: int,
    start_date,
    end_date
):
    logs = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.well_id == well_id,
            ProductionLog.log_date >= start_date,
            ProductionLog.log_date <= end_date,
            ProductionLog.is_active == True
        )
        .all()
    )

    if not logs:
        return None

    total_oil = sum(log.oil_bbl for log in logs)
    total_water = sum(log.water_bbl for log in logs)

    total_days = len(logs)

    average_daily_oil = total_oil / total_days if total_days else 0

    total_fluids = total_oil + total_water
    water_cut = (total_water / total_fluids) if total_fluids > 0 else 0

    downtime_days = sum(
        1 for log in logs
        if log.oil_bbl == 0 and log.water_bbl == 0 and log.gas_mscf == 0
    )

    water_cut_alert = water_cut > WATER_CUT_ALERT_THRESHOLD

    return {
        "well_id": well_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_oil_bbl": total_oil,
        "average_daily_oil_bbl": average_daily_oil,
        "water_cut": water_cut,
        "downtime_days": downtime_days,
        "water_cut_alert": water_cut_alert
    }

def get_monthly_production_summary(
    db: Session,
    well_id: int,
    year: int,
    month: int
):
    logs = (
        db.query(ProductionLog)
        .filter(
            ProductionLog.well_id == well_id,
            extract("year", ProductionLog.log_date) == year,
            extract("month", ProductionLog.log_date) == month,
            ProductionLog.is_active == True
        )
        .all()
    )

    if not logs:
        return None

    total_oil = sum(log.oil_bbl for log in logs)
    total_gas = sum(log.gas_mscf for log in logs)
    total_water = sum(log.water_bbl for log in logs)

    days_count = len(logs)

    average_daily_oil = total_oil / days_count if days_count else 0

    total_fluids = total_oil + total_water
    water_cut = (total_water / total_fluids) if total_fluids > 0 else 0

    downtime_days = sum(
        1 for log in logs
        if log.oil_bbl == 0 and log.gas_mscf == 0 and log.water_bbl == 0
    )

    return {
        "well_id": well_id,
        "year": year,
        "month": month,
        "total_oil_bbl": total_oil,
        "total_gas_mscf": total_gas,
        "total_water_bbl": total_water,
        "average_daily_oil_bbl": average_daily_oil,
        "water_cut": water_cut,
        "downtime_days": downtime_days
    }

def get_water_cut_trend(db, well_id: int, days: int):
    start_date = date.today() - timedelta(days=days)

    rows = (
        db.query(
            ProductionLog.log_date.label("date"),
            func.sum(ProductionLog.oil_bbl).label("oil"),
            func.sum(ProductionLog.water_bbl).label("water"),
        )
        .filter(
            ProductionLog.well_id == well_id,
            ProductionLog.log_date >= start_date,
            ProductionLog.is_active == True
        )
        .group_by(ProductionLog.log_date)
        .order_by(ProductionLog.log_date)
        .all()
    )

    data = []
    for r in rows:
        total = r.oil + r.water
        water_cut = (r.water / total) if total > 0 else None

        data.append({
            "date": r.date,
            "oil_bbl": r.oil,
            "water_bbl": r.water,
            "water_cut": round(water_cut, 3) if water_cut is not None else None
        })

    return data