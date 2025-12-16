from db.session import engine
from db.base import Base
from db.models import field, well, production_log

Base.metadata.create_all(bind=engine)
