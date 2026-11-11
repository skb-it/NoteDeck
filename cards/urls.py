from rest_framework import routers

from cards.views import CardViewSet, DeckViewSet, NoteViewSet

router = routers.DefaultRouter()
router.register("decks", DeckViewSet, basename="deck")
router.register("cards", CardViewSet, basename="card")
router.register("notes", NoteViewSet, basename="note")

urlpatterns = router.urls
