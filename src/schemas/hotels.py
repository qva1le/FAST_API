from fastapi import Body
from pydantic import BaseModel, Field, ConfigDict

class  HotelAdd(BaseModel):
    title: str = Body(...),
    location: str = Body(...)


class  Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
