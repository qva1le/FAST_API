from src.services.auth import AuthServices


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthServices().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthServices().decode_token(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]