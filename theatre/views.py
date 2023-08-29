from rest_framework import viewsets

from theatre.models import TheatreHall, Genre, Actor, Play, Performance
from theatre.serializers import (
    TheatreHallSerializer,
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    PerformanceSerializer
)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
