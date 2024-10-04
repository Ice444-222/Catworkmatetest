from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CatViewSet, BreedViewSet, RatingViewSet)

router = DefaultRouter()
router.register("cats", CatViewSet, basename="cats")
router.register("breeds", BreedViewSet, basename="breeds")
router.register("ratings", RatingViewSet, basename="ratings")

urlpatterns = [
    path("", include(router.urls)),
]
