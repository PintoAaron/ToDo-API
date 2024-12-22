import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Task


@pytest.mark.django_db
class TestCreateTask():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        data = {'name': 'Go To Cinema',
                'description': 'go to silverbird to watch the new Avengers movie',
                'is_done': False
                }
        response = api_client.post('/api/v1/todo/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate()
        data = {'name': 'Go To Cinema'
                }
        response = api_client.post('/api/v1/todo/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'description' in response.data

    def test_if_user_is_authenticated(self, api_client, authenticate):
        authenticate()
        data = {'name': 'Go To Cinema',
                'description': 'go to silverbird to watch the new Avengers movie',
                'is_done': False
                }
        response = api_client.post('/api/v1/todo/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestListHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        response = api_client.get('/api/v1/todo/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_return_200(self, api_client, authenticate):
        authenticate()
        task = baker.make(Task)
        response = api_client.get('/api/v1/todo/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetriveHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        response = api_client.get(f'/api/v1/todo/{task.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_return_200(self, api_client, authenticate):
        authenticate()
        task = baker.make(Task)
        response = api_client.get(f'/api/v1/todo/{task.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == task.id

    def test_if_task_does_not_exist_return_404(self, api_client, authenticate):
        authenticate()
        response = api_client.get('/api/v1/todo/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateHostel:
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        data = {'name': 'Updated Task'}
        response = api_client.patch(f'/api/v1/todo/{task.id}/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_return_200(self, api_client, authenticate):
        authenticate()
        task = baker.make(Task)
        data = {'name': 'Updated Task'}
        response = api_client.patch(f'/api/v1/todo/{task.id}/', data)
        assert response.status_code == status.HTTP_200_OK

    def test_if_task_does_not_exist_return_404(self, api_client, authenticate):
        authenticate()
        response = api_client.patch(
            '/api/v1/todo/1/', {'name': 'Updated Task'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'


@pytest.mark.django_db
class TestDeleteHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        task = baker.make(Task)
        response = api_client.delete(f'/api/v1/todo/{task.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_return_204(self, api_client, authenticate):
        authenticate()
        task = baker.make(Task)
        response = api_client.delete(f'/api/v1/todo/{task.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_hostel_does_not_exist_return_404(self, api_client, authenticate):
        authenticate()
        response = api_client.delete('/api/v1/todo/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
