from fastapi import FastAPI
from app.routers import field, well, production_log

app = FastAPI()

app.include_router(field.router)
app.include_router(well.router)
app.include_router(production_log.router)