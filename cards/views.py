from rest_framework import permissions, viewsets

from .models import Card
from .serializers import CardSerializer, DeckSerializer


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.decks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(deck__owner=self.request.user)
