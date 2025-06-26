import pytest

@pytest.mark.parametrize("email, password", [
    ("qwe@example.com", "12345"),
    ("rop@mail.ru", "12345"),
])
async def test_all_auth(
        email, password,
        register_user,
        ac
):
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )

    assert response_register.status_code == 200


    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )

    assert response_login.status_code == 200
    assert "access_token" in ac.cookies

    response_me = await ac.get(
        "/auth/me"
    )

    assert response_me.status_code == 200
    assert response_me.json()["email"] == email

    response_logout = await ac.get(
        "/auth/logout",
    )

    assert response_logout.status_code == 200
    assert "access_token" not in ac.cookies

    response_register_again = await ac.post(
        "/auth/register",
        json = {
            "email": email,
            "password": password,
        }
    )

    assert response_register_again.status_code == 400
    assert response_register_again.json()["detail"] == "Пользователь с таким email уже зарегистрирован"

    response_me_again = await ac.get(
        "/auth/me",
    )
    assert response_me_again.status_code == 401




