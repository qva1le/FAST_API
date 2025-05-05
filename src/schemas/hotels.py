from fastapi import Body
from pydantic import BaseModel, Field

class  Hotel(BaseModel):
    title: str = Body(...),
    location: str = Body(...)

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)