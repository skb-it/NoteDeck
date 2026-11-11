from rest_framework import permissions, viewsets

from .models import Card, Note
from .serializers import CardSerializer, DeckSerializer, NoteSerializer

class DeckOwnerQuerysetMixin:
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(deck__owner=self.request.user)
class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.decks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteViewSet(DeckOwnerQuerysetMixin, viewsets.ModelViewSet):
    model = Note
    serializer_class = NoteSerializer

class CardViewSet(DeckOwnerQuerysetMixin, viewsets.ModelViewSet):
    model = Card
    serializer_class = CardSerializer
