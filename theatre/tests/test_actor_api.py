from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Actor
from theatre.serializers import ActorSerializer


ACTOR_URL = reverse("theatre:actor-list")


class UnAuthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_actors(self):
        Actor.objects.create(first_name="Test", last_name="1")
        Actor.objects.create(first_name="Test", last_name="2")

        res = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_actor_forbidden(self):
        payload = {"first_name": "Test", "last_name": "Actor"}
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@mate.com", "password", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_actor(self):
        payload = {"first_name": "Test", "last_name": "Actor"}
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        actor = Actor.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(actor, key))
