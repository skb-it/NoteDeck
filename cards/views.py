from django.db import transaction
from rest_framework import permissions, viewsets

from .chunking import chunk_text
from .models import Card, Chunk, Note
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

    def perform_create(self, serializer):
        with transaction.atomic():
            note = serializer.save()
            note_chunked = chunk_text(note.content)

            chunks = []

            for counter, chunk in enumerate(note_chunked):
                chunks.append(Chunk(content=chunk, note=note, seq_number=counter))

            Chunk.objects.bulk_create(chunks)


class CardViewSet(DeckOwnerQuerysetMixin, viewsets.ModelViewSet):
    model = Card
    serializer_class = CardSerializer
