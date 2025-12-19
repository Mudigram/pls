from pydantic import BaseModel
from datetime import date


class WellProductionSummary(BaseModel):
    well_id: int
    start_date: date
    end_date: date

    total_oil_bbl: float
    average_daily_oil_bbl: float
    water_cut: float
    downtime_days: int
    water_cut_alert: bool

class MonthlyProductionSummary(BaseModel):
    well_id: int
    year: int
    month: int

    total_oil_bbl: float
    total_gas_mscf: float
    total_water_bbl: float

    average_daily_oil_bbl: float
    water_cut: float
    downtime_days: int
