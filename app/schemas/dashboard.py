from pydantic import BaseModel
from datetime import date
from typing import List


class CategorySummary(BaseModel):
    category_id: int
    category_name: str
    total_amount: float


class DailySummary(BaseModel):
    date: date
    total_amount: float


class DashboardResponse(BaseModel):
    year: int
    month: int
    monthly_total: float
    by_category: List[CategorySummary]
    daily: List[DailySummary]
