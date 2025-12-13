"""
Unit tests for backend.app.security
"""
# pylint: disable=invalid-name, missing-function-docstring, import-error
import jwt
from backend.app.security import create_jwt_token, ALGORITHM, verify_password, get_password_hash


def test_create_jwt_token(mocker):
    test_subject = "test_subject"
    test_key = "foobar"
    mocker.patch("backend.app.security.SECRET_KEY", test_key)

    token = create_jwt_token(test_subject)
    decoded_token = jwt.decode(token, test_key, ALGORITHM)
    assert decoded_token["subject"] == test_subject


def test_password_verification():
    test_password = "foobar"
    test_hash = get_password_hash(test_password)

    assert verify_password(test_password, test_hash)
