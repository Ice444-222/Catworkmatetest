import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from cats.models import Cat, Breed


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(username, is_staff=False):
        return User.objects.create_user(
            username=username, password="cattestpassword", is_staff=is_staff
        )
    return make_user


@pytest.fixture
def breed(db):
    return Breed.objects.create(
        name="Бенгал", description="Очень активная порода"
    )


@pytest.fixture
def cat(create_user, breed):
    user = create_user(username="testuser")
    return Cat.objects.create(
        name="Testcat", color="Ginger", birth_date="2024-01-01",
        description="Молодой котенок", breed=breed, author=user
    )


@pytest.fixture
def jwt_token(api_client, create_user):
    def get_token(
            username="test_user", password="cattestpassword", is_staff=False):
        user = create_user(username=username, is_staff=is_staff)
        response = api_client.post('/auth/jwt/create/', {
            "username": user.username,
            "password": "cattestpassword"
        }, format='json')

        assert response.status_code == 200
        return response.data['access']
    return get_token


@pytest.mark.django_db
class TestCatAPI:

    def test_create_cat(self, api_client, jwt_token, breed):
        token = jwt_token(username="author_user")
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.post('/api/cats/', {
            "name": "Пушок",
            "color": "Gray",
            "birth_date": "2024-06-01",
            "description": "Спокойный кот",
            "breed": breed.id
        }, format='json')

        assert response.status_code == 201
        assert response.data['name'] == 'Пушок'
        assert response.data['color'] == 'Gray'

    def test_list_cats(self, api_client, cat):
        response = api_client.get('/api/cats/')
        assert response.status_code == 200
        assert len(response.data) > 0
        assert response.data[0]['name'] == cat.name

    def test_retrieve_cat(self, api_client, cat):
        response = api_client.get(f'/api/cats/{cat.id}/')
        assert response.status_code == 200
        assert response.data['name'] == cat.name

    def test_filter_cats_by_breed(self, api_client, breed, cat):
        response = api_client.get(f'/api/cats/?breed={breed.name}')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['breed'] == breed.name

    def test_permission_restrictions(
            self, api_client, cat, jwt_token
    ):
        token = jwt_token(username="other_user")
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.patch(
            f'/api/cats/{cat.id}/', {"name": "Updated Name"}
        )
        assert response.status_code == 403


@pytest.mark.django_db
class TestRatingAPI:

    def test_create_rating(self, api_client, cat, jwt_token):
        token = jwt_token(username="author_user")
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.post('/api/ratings/', {
            "cat": cat.id,
            "score": 5
        }, format='json')

        assert response.status_code == 201
        assert response.data['score'] == 5

    def test_list_user_ratings(self, api_client, cat, jwt_token):
        token = jwt_token(username="author_user")
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        api_client.post(
            '/api/ratings/', {"cat": cat.id, "score": 5}, format='json'
        )

        response = api_client.get('/api/ratings/')
        assert response.status_code == 200
        assert len(response.data) > 0
        assert response.data[0]['score'] == 5

    def test_admin_delete_rating(self, api_client, cat, jwt_token):
        token = jwt_token(username="author_user")
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.post(
            '/api/ratings/', {"cat": cat.id, "score": 4}, format='json'
        )
        assert response.status_code == 201
        rating_id = response.data['id']

        token = jwt_token(username="admin", is_staff=True)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.delete(f'/api/ratings/{rating_id}/')
        assert response.status_code == 204
