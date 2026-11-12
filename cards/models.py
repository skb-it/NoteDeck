from django.conf import settings
from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="decks", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    deck = models.ForeignKey(Deck, related_name="notes", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    deck = models.ForeignKey(Deck, related_name="cards", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]


class Chunk(models.Model):
    note = models.ForeignKey(Note, related_name="chunks", on_delete=models.CASCADE)
    seq_number = models.PositiveIntegerField()
    content = models.TextField()
