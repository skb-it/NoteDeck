from rest_framework import viewsets, permissions
from .serializers import DeckSerializer


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.decks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


