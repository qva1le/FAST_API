from fastapi import APIRouter, Query
from src.api.dependecies import DBDep
from src.schemas.facilities import FacilitiesAddRequest

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
        facility_id: int | None = Query(None, description="Айдишник удобства" ),
):
   if facility_id is None:
       return await db.facilities.get_all()
   else:
       return await db.facilities.get_filtered(id=facility_id)

@router.post("")
async def create_facility(title_data: FacilitiesAddRequest, db: DBDep):
    facility = await db.facilities.add(title_data)
    await db.commit()
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