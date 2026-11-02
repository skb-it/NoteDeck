from django.contrib import admin
from django.contrib.messages import api
from django.urls import path, include
from cards.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls"))
]
