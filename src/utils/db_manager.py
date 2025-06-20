from src.repositories.hotels import HotelsRepository
from src.repositories.mappers.mappers import BookingDataMapper, HotelDataMapper, RoomDataMapper, UserDataMapper, \
    FacilitiesDataMapper
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository
from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import FacilitiesRepository
from src.repositories.rooms_facilities import RoomsFacilitiesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session, mapper=HotelDataMapper)
        self.rooms = RoomsRepository(self.session, mapper=RoomDataMapper)
        self.users = UsersRepository(self.session, mapper=UserDataMapper)
        self.bookings = BookingsRepository(self.session, mapper=BookingDataMapper)
        self.facilities = FacilitiesRepository(self.session, mapper=FacilitiesDataMapper)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session, mapper=None)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()



    async def commit(self):
        await self.session.commit()
