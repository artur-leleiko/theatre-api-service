from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    TheatreHallViewSet,
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    PerformanceViewSet
)

router = routers.DefaultRouter()
router.register("theatre_halls", TheatreHallViewSet)
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
