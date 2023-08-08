from django.urls import path
from .views import DatabaseAPI, ArtifactAPI, CollectionSerializerAPI

urlpatterns = [
    path('database/', DatabaseAPI.as_view()),
    path('<int:db>/artifact/', ArtifactAPI.as_view()),
    path('<int:atr>/collection', CollectionSerializerAPI.as_view()),
]