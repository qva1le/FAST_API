from fastapi import FastAPI, Body, Query, APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import insert, select
from src.api.dependecies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch
from src.models.hotels import HotelsOrm
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("", summary="Получение отелей", description="<h1>Тут мы получаем все отели, которые у нас есть<h1>")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация отеля"),
        title: str | None = Query(None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
       return await HotelsRepository(session).get_all(
           location=location,
           title=title,
           limit=per_page,
           offset=per_page * (pagination.page - 1)
       )

@router.post("", summary="Создание отеля", description="<h1>Тут мы создаем отель<h1>")
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звёзд у моря",
                    "location": "ул. Моря, 1",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай 5 звёзд у моря",
                    "location": "ул. Шейха, 2",
                }
            }
        })

):
    async with async_session_maker() as session:
         hotel = await HotelsRepository(session).add(hotel_data)
         await session.commit()

    return {"status": "OK", "hotel": hotel}



@router.put("/{hotel_id}", summary="Изменение всего отеля", description="<h1>Тут мы изменяем весь отель<h1>")
def edit_hotel(
       hotel_id: int,
       hotel_data: Hotel,

):

    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels[i] = {
                "id": hotel_id,
                "title": hotel_data.title,
                "name": hotel_data.name,
            }
            return {"status": "OK", "hotel": hotels[i]}
    return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}



@router.patch("/{hotel_id}", summary="Изменение одного поля отеля, но не обязательно", description="<h1>Тут мы изменяем одно поле отеля<h1>")
def update_hotel_field(
       hotel_id: int,
       hotel_data: HotelPatch,
):

    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotels[i]["title"] = hotel_data.title
            return {"status": "OK", "hotel": hotels[i]}
    return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}



@router.delete("/{hotel_id}", summary="Удаление отеля", description="<h1>Тут мы удаляем отель<h1>")
def delete_hotel_id(hotel_id: int):
    global hotels
    for hotel in hotels:
        if hotel["id"] != id:
            return {"status": "OK"}