from django.urls import path
from .views import DatabaseAPI, ArtifactAPI, CollectionSerializerAPI, CollectionSerializerDataAPI

urlpatterns = [
    path('database/', DatabaseAPI.as_view()),
    path('<db>/artifact/', ArtifactAPI.as_view()),
    path('<atr>/collection', CollectionSerializerAPI.as_view()),
    path('<col>/collection-data', CollectionSerializerDataAPI.as_view())
]