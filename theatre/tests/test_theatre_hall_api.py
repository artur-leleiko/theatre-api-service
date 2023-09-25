from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import TheatreHall
from theatre.serializers import TheatreHallSerializer

THEATRE_HALL_URL = reverse("theatre:theatrehall-list")


def sample_theatre_hall(**params):
    defaults = {
        "name": "Test Theatre Hall",
        "rows": 15,
        "seats_in_row": 15
    }
    defaults.update(**params)

    return TheatreHall.objects.create(**defaults)


class UnAuthenticatedTheatreHallApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(THEATRE_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTheatreHallApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_theatre_halls(self):
        sample_theatre_hall(name="Test1")
        sample_theatre_hall(name="Test2")

        res = self.client.get(THEATRE_HALL_URL)

        theatre_halls = TheatreHall.objects.all()
        serializer = TheatreHallSerializer(theatre_halls, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_theatre_hall_forbidden(self):
        payload = {"name": "Test", "rows": 15, "seats_in_row": 15}
        res = self.client.post(THEATRE_HALL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTheatreHallApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@mate.com", "password", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_theatre_hall(self):
        payload = {"name": "Test", "rows": 15, "seats_in_row": 15}
        res = self.client.post(THEATRE_HALL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        theatre_hall = TheatreHall.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(theatre_hall, key))
