from rest_framework import routers
from cards.views import DeckViewSet


router = routers.DefaultRouter()
router.register("decks", DeckViewSet, basename="deck")

urlpatterns = router.urls
