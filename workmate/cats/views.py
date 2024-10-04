
from rest_framework import permissions, viewsets
from .models import Cat, Breed, Rating
from .serializers import CatSerializer, CatGetSerializer, BreedSerializer, RatingSerializer
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CatFilter


class CatViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CatGetSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BreedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
