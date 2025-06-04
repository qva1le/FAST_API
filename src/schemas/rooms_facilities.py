from pydantic import BaseModel



class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacility(RoomFacilityAdd):
    id: int

