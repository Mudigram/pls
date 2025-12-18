from app.services.production_log_services import (
    create_production_log,
    revise_production_log,
)
from app.schemas.production_log import ProductionLogUpdate
from fastapi import HTTPException
from datetime import date
from typing import cast
import pytest

def test_create_production_log(db):
    log = create_production_log(
        db=db,
        well_id=1,
        production_date=date(2025, 1, 1),
        oil_bbl=100,
        gas_mscf=50,
        water_bbl=20,
    )

    assert log.id is not None
    assert cast(int, log.well_id) == 1
    assert cast(float, log.oil_bbl) == 100.0
    assert cast(float, log.gas_mscf) == 50.0
    assert cast(float, log.water_bbl) == 20.0
    assert cast(bool, log.is_active) is True
    assert cast(int, log.revision_count) == 0


def test_duplicate_production_log_not_allowed(db):
    create_production_log(
        db=db,
        well_id=1,
        production_date=date(2025, 1, 1),
        oil_bbl=100,
        gas_mscf=50,
        water_bbl=20,
    )

    with pytest.raises(ValueError):
        create_production_log(
            db=db,
            well_id=1,
            production_date=date(2025, 1, 1),
            oil_bbl=150,
            gas_mscf=60,
            water_bbl=30,
        )

def test_revise_production_log_creates_new_revision(db):
    original = create_production_log(
        db=db,
        well_id=1,
        production_date=date.today(),
        oil_bbl=100,
        gas_mscf=50,
        water_bbl=20,
    )

    update = ProductionLogUpdate(
        oil_bbl=120
    )

    revised = revise_production_log(
        db=db,
        log_id=original.id,
        update=update
    )

    # New record created
    assert cast(int, revised.id) != original.id
    assert cast(float, revised.oil_bbl) == 120.0
    assert cast(float, revised.gas_mscf) == 50.0
    assert cast(float, revised.water_bbl) == 20.0

    # Revision metadata
    assert cast(int, revised.revision_count) == 1
    assert cast(bool, revised.is_active) is True

    # Old log retired
    db.refresh(original)
    assert cast(bool, original.is_active) is False

   
    