from pydantic import BaseModel, ConfigDict


class FacilitiesAddRequest(BaseModel):

    title: str

    model_config = ConfigDict(from_attributes=True)

class FacilitiesAdd(BaseModel):
    room_id: int
    title: str