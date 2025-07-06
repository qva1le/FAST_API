from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, facility_data: FacilitiesAdd):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()
        return facility
