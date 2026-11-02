from rest_framework import routers

from cards.views import CardViewSet, DeckViewSet

router = routers.DefaultRouter()
router.register("decks", DeckViewSet, basename="deck")
router.register("cards", CardViewSet, basename="card")
urlpatterns = router.urls
