from fastapi import APIRouter, Query
from src.api.dependecies import DBDep
from src.schemas.facilities import FacilitiesAddRequest, FacilitiesAdd

router = APIRouter(prefix="/hotels/{hotel_id}/rooms/{room_id}", tags=["Удобства"])


@router.get("/facilities")
async def get_facilities(
        db: DBDep,
        facility_id: int | None = Query(None, description="Айдишник удобства" ),
):
   if facility_id is None:
       return await db.facilities.get_all()
   else:
       return await db.facilities.get_filtered(id=facility_id)

@router.post("/facilities")
async def create_facility(title: FacilitiesAddRequest, db: DBDep):
    facility = await db.facilities.add(title)
    await db.commit()
    return {"status": "OK", "facility": facility}