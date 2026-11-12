from rest_framework import serializers

from .models import Card, Deck, Note


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ("id", "name", "owner", "created_at")
        read_only_fields = ("owner",)


class OwnedDeckMixin:
    def validate_deck(self, value):
        user = self.context["request"].user
        if value.owner != user:
            raise serializers.ValidationError("You can only use your own decks.")
        return value


class CardSerializer(OwnedDeckMixin, serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "deck", "question", "answer", "created_at")


class NoteSerializer(OwnedDeckMixin, serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "deck", "name", "content", "created_at")
