from src.schemas.facilities import FacilitiesAdd, FacilitiesAddRequest

async def test_post_facilities(db):
    facility_data = FacilitiesAddRequest(
        title="Бесплатный Бар"
    )
    await db.facilities.add(facility_data)

    assert facility_data

async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200