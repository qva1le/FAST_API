from src.models.facilities import RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms_facilities import RoomsFacilitiesAddRequest


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilitiesAddRequest
