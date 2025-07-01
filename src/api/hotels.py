from datetime import date

from fastapi import FastAPI, Body, Query, APIRouter, HTTPException

from fastapi_cache.decorator import cache

from src.api.dependecies import PaginationDep, DBDep
from src.exceptions import DatesAreIncorrect, HotelDoesNotExist
from src.repositories.mappers.mappers import HotelDataMapper
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("", summary="Получение отелей", description="<h1>Тут мы получаем все отели, которые у нас есть<h1>")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация отеля"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2025-06-01"),
        date_to: date = Query(example="2025-06-05"),

):
        if date_from >= date_to:
            raise HTTPException(status_code=409, detail=DatesAreIncorrect.detail)
        per_page = pagination.per_page or 5
        return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel

@router.post("", summary="Создание отеля", description="<h1>Тут мы создаем отель<h1>")
async def create_hotel(
        db: DBDep,hotel_data: HotelAdd = Body(openapi_examples={
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
         hotel = await db.hotels.add(hotel_data)
         await db.commit()
         return {"status": "OK", "hotel": hotel}

@router.put("/{hotel_id}", summary="Изменение всего отеля", description="<h1>Тут мы изменяем весь отель<h1>")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
        await db.hotels.edit(hotel_data,id=hotel_id)
        await db.commit()
        return {"status": "OK"}

@router.patch("/{hotel_id}", summary="Изменение одного поля отеля, но не обязательно", description="<h1>Тут мы изменяем одно поле отеля<h1>")
async def update_hotel_field(
       hotel_id: int,
       hotel_data: HotelPatch,
        db: DBDep
):
        await db.hotels.edit(hotel_data,exclude_unset=True,id=hotel_id)
        await db.commit()
        return {"status": "OK"}

@router.delete("/{hotel_id}", summary="Удаление отеля", description="<h1>Тут мы удаляем отель<h1>")
async def delete_hotel_id(hotel_id: int, db: DBDep):
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"status": "OK"}