from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilitiesDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper
