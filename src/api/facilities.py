import json

from fastapi import APIRouter, Query

from fastapi_cache.decorator import cache

from src.api.dependecies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesAddRequest
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
#@cache(expire=10)
async def get_facilities(
        db: DBDep,
        facility_id: int | None = Query(None, description="Айдишник удобства" ),
):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(title_data: FacilitiesAddRequest, db: DBDep):
    facility = await db.facilities.add(title_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "facility": facility}



# @router.put("")
# async def edit_facility(facility_id: int, title_data: FacilitiesAddRequest, db: DBDep):
#     await db.facilities.edit(title_data, id=facility_id)
#     await db.commit()
#     return {"status": "OK"}
#
# @router.delete("")
# async def delete_facility(facility_id: int, db: DBDep):
#     await db.facilities.delete(id=facility_id)
#     await db.commit()
#     return {"status": "OK"}