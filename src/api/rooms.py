from datetime import date

from fastapi import FastAPI, Body, Query, APIRouter, HTTPException

from src.api.dependecies import PaginationDep, DBDep
from src.exceptions import RoomDoesNotExist, ObjectNotFoundException, HotelDoesNotExist, RoomNotFoundException, \
    HotelNotFoundException, HotelNotFoundHTTPException
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.rooms_facilities import RoomFacilityAdd, RoomFacility
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundException

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        room = await RoomService(db).add_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "room": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    await RoomService(db).edit_room(hotel_id,room_id,room_data)
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    await RoomService(db).partially_edit_room(hotel_id,room_id, room_data)

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}



