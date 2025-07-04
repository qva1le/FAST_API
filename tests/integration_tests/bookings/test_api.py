import pytest
from sqlalchemy import delete

from src.models.bookings import BookingsOrm
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (2, "2024-08-01", "2024-08-10", 200),
    (3, "2024-08-01", "2024-08-10", 500),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res

@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, expected_status", [
    (1, "2024-08-01", "2024-08-10", 1),
    (2, "2025-08-01", "2025-08-10", 2),
    (1, "2024-08-01", "2024-08-10", 3),
])
async def test_add_and_get_bookings(
    room_id, date_from, date_to, expected_status,
    delete_all_bookings,
    db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res

    response_me = await authenticated_ac.get("/bookings/me")
    assert response_me.status_code == 200
    bookings = response_me.json()
    assert isinstance(bookings, list)
    assert len(bookings) >= 1
