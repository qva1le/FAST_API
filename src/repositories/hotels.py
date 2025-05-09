from sqlalchemy import select, func, insert


from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return   result.scalars().all()

    async def add(
            self,
            title,
            location,
    ):
       add_hotel = insert(HotelsOrm).values(
           title=title,
           location=location,
       )
       await self.session.execute(add_hotel)



