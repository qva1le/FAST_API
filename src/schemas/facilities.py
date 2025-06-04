from pydantic import BaseModel, ConfigDict


class FacilitiesAddRequest(BaseModel):

    title: str

    model_config = ConfigDict(from_attributes=True)

class FacilitiesAdd(BaseModel):
    facility_id: int
    title: str

class Facility(FacilitiesAddRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)