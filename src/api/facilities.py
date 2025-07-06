import json

from fastapi import APIRouter, Query

from fastapi_cache.decorator import cache

from src.api.dependecies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesAddRequest, FacilitiesAdd
from src.services.facilities import FacilityService
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(
        db: DBDep,
        facility_id: int | None = Query(None, description="Айдишник удобства" ),
):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(title_data: FacilitiesAddRequest, db: DBDep):
    facility = await FacilityService(db).create_facility(title_data)
    return {"status": "OK", "facility": facility}


