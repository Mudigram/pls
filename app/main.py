from fastapi import FastAPI
from app.routers import field, well, production_log, reports

app = FastAPI(title="Production Log System", description="API for managing production logs", version="1.0.0")

app.include_router(field.router)
app.include_router(well.router)
app.include_router(production_log.router)
app.include_router(reports.router)