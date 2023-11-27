from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Genre
from theatre.serializers import GenreSerializer

GENRE_URL = reverse("theatre:genre-list")


class UnAuthenticatedGenreApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedGenreApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_genres(self):
        Genre.objects.create(name="Test1")
        Genre.objects.create(name="Test2")

        res = self.client.get(GENRE_URL)

        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_genre_forbidden(self):
        payload = {"name": "Genre"}
        res = self.client.post(GENRE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@mate.com", "password", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_genre(self):
        payload = {"name": "Genre"}
        res = self.client.post(GENRE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        genre = Genre.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(genre, key))
