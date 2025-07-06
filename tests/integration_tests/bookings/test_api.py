import pytest
from tests.conftest import get_db_null_pool


async def test_add_booking_with_conflict(authenticated_ac):
    response_1 = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": 3,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response_1.status_code == 200

    response_2 = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": 3,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response_2.status_code == 200


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


async def test_add_and_get_bookings(authenticated_ac, delete_all_bookings):
    resp1 = await authenticated_ac.post("/bookings", json={
        "room_id": 1,
        "date_from": "2024-08-01",
        "date_to": "2024-08-10",
    })
    assert resp1.status_code == 200

    resp2 = await authenticated_ac.post("/bookings", json={
        "room_id": 1,
        "date_from": "2024-08-01",
        "date_to": "2024-08-10",
    })
    assert resp2.status_code == 200

    response_me = await authenticated_ac.get("/bookings/me")
    assert response_me.status_code == 200
    bookings = response_me.json()
    assert isinstance(bookings, list)
    assert len(bookings) == 2
