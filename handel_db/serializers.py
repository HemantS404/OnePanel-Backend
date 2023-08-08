from rest_framework import serializers
from .models import Database, Artifact, Collection

class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = "__all__"

class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = "__all__"

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"