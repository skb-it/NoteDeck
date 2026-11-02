from rest_framework import serializers

from .models import Card, Deck


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ("id", "name", "owner", "created_at")
        read_only_fields = ("owner",)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "deck", "question", "answer", "created_at")

    def validate_deck(self, value):
        user = self.context["request"].user
        if value.owner != user:
            raise serializers.ValidationError(
                {"error": "You are not authorized to add this card"}
            )
        return value
