import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Task


url = '/api/v1/todo/'


@pytest.mark.django_db
class TestCreateTask():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        data = {'name': 'Go To Cinema',
                'description': 'go to silverbird to watch the new Avengers movie',
                'is_done': False
                }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate()
        data = {'name': 'Go To Cinema'
                }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'description' in response.data

    def test_if_user_is_authenticated(self, api_client, authenticate):
        authenticate()
        data = {'name': 'Go To Cinema',
                'description': 'go to silverbird to watch the new Avengers movie',
                'is_done': False
                }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestListHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_return_200(self, api_client, authenticate):
        authenticate()
        task = baker.make(Task)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetriveHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        response = api_client.get(url + f'{task.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_task_does_not_exist_return_404(self, api_client, authenticate):
        authenticate()
        response = api_client.get(url + '100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateHostel:
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        data = {'name': 'Updated Task'}
        response = api_client.patch(url + f'{task.id}/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
