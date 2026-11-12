from django.db import transaction
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .chunking import chunk_text
from .models import Card, Chunk, Note
from .serializers import CardSerializer, DeckSerializer, NoteSerializer
from .llm import generate_cards as llm_generate_cards

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

    @action(detail=True, methods=["post"], url_path="generate-cards")
    def generate_cards(self, request, pk=None):
        note = self.get_object()

        cards_list = []

        for chunk in note.chunks.all():
            cards = llm_generate_cards(chunk.content)
            for card in cards:
                card_obj = Card(question=card["question"], answer=card["answer"], deck=note.deck)
                cards_list.append(card_obj)

        created = Card.objects.bulk_create(cards_list)
        return Response(CardSerializer(created, many=True).data, status=201)

class CardViewSet(DeckOwnerQuerysetMixin, viewsets.ModelViewSet):
    model = Card
    serializer_class = CardSerializer
