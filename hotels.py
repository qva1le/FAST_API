from fastapi import FastAPI, Body, Query, APIRouter
from pydantic import BaseModel, Field
from pygments.lexer import default

from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])



hotels = [
     {"id": 1, "title": "Sochi", "name": "sochi"},
     {"id": 2, "title": "Дубай", "name": "dubai"},
     {"id": 3, "title": "Мальдивы", "name": "maldivi"},
     {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
     {"id": 5, "title": "Москва", "name": "moscow"},
     {"id": 6, "title": "Казань", "name": "kazan"},
     {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
 ]



@router.get("", summary="Получение отелей", description="<h1>Тут мы получаем все отели, которые у нас есть<h1>")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(1, description="Номер страницы"),
        per_page: int | None = Query(5, description="Количество отелей на странице"),
):

    global hotels
    for hotel in hotels:
        if hotel["id"] == id or hotel["title"] == title:
            return hotel
    return hotels[page * per_page - per_page: page * per_page]
    # 1 * 5 - 5



@router.post("", summary="Создание отеля", description="<h1>Тут мы создаем отель<h1>")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}



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