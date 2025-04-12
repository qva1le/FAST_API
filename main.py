from imp import reload

from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI()
hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]



@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    for hotel in hotels:
        if hotel["id"] == id or hotel["title"] == title:
            return hotel
    return hotels


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}")
def edit_hotel(
       hotel_id: int,
       title: str = Body(...),
       name: str = Body(...)
):

    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            hotels[i] = {
                "id": hotel_id,
                "title": title,
                "name": name
            }
            return {"status": "OK", "hotel": hotels[i]}
    return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}

@app.patch("/hotels/{hotel_id}")
def update_hotel_field(
       hotel_id: int,
       title: str | None = Body(default=None),
):

    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if title is not None:
                hotels[i]["title"] = title
            return {"status": "OK", "hotel": hotels[i]}
    return {"status": "error", "message": f"Hotel with id {hotel_id} not found"}




@app.delete("/hotels/{hotel_id}")
def delete_hotel_id(hotel_id: int):
    global hotels
    for hotel in hotels:
        if hotel["id"] != id:
            return {"status": "OK"}





if __name__ == '__main__':
    uvicorn.run("main:app" ,reload=True)