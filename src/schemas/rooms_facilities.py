from pydantic import BaseModel



class RoomsFacilitiesAddRequest(BaseModel):
    room_id: int
    title: str