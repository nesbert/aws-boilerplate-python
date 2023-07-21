import pytest
import requests
import requests_mock

from gorest import users

BASE_URL = users.BASE_URL
RESOURCE_URL = users.RESOURCE_URL


def test_fetch():
    with requests_mock.Mocker() as mock:
        user_id = 1
        mock_response = {
            "id": 42,
            "name": "Miles Morales",
            "email": "spiderman@earth-1610",
            "gender": "male",
            "status": "active",
        }
        mock.get(f"{RESOURCE_URL}/{user_id}", json=mock_response)

        result = users.fetch(user_id)
        assert result == mock_response


def test_fetch_all():
    with requests_mock.Mocker() as mock:
        mock_response = {
            "data": [
                {"id": 1610, "name": "Miles Morales"},
                {"id": 65, "name": "Gwendolyn Stacy"},
            ]
        }
        mock.get(f"{RESOURCE_URL}?page=1&per_page=2", json=mock_response)

        response = users.fetch_all(1, 2)
        assert response == mock_response


def test_fetch_all_no_params():
    with requests_mock.Mocker() as mock:
        mock_response = {"data": "all_users_data"}
        mock.get(RESOURCE_URL, json=mock_response)

        result = users.fetch_all()
        assert result == mock_response


def test_fetch_raises_exception_for_http_error():
    with requests_mock.Mocker() as mock:
        mock.get(f"{RESOURCE_URL}/1", status_code=404)

        with pytest.raises(requests.exceptions.HTTPError):
            users.fetch(1)


def test_fetch_all_raises_exception_for_http_error():
    with requests_mock.Mocker() as mock:
        mock.get(f"{RESOURCE_URL}?page=1&per_page=2", status_code=404)

        with pytest.raises(requests.exceptions.HTTPError):
            users.fetch_all(1, 2)
