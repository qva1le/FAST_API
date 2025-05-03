from fastapi import Body
from pydantic import BaseModel, Field

class  Hotel(BaseModel):
    title: str = Body(...),
    name: str = Body(...)

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)