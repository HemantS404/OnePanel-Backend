from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from .models import Database, Artifact, Collection
from .serializers import DatabaseSerializer, ArtifactSerializer, CollectionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
import json
from accounts.permisions import IsVerified
# Create your views here.

class DatabaseAPI(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = DatabaseSerializer
    queryset = Database.objects

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset
    
    def post(self, request):
        serializer = self.serializer_class(data = {"name":request.data.get('name'), "user":request.user.id})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    def get(self, request):
        return self.list(request)
    
class ArtifactAPI(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = ArtifactSerializer
    queryset = Artifact.objects

    def post(self, request, db):
        serializer = self.serializer_class(data = {"name":request.data.get('name'), "database":db})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    def get(self, request, db):
        serializer = self.serializer_class(self.queryset.filter(database = db), many=True)
        return Response(serializer.data)
    
class CollectionSerializerAPI(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = CollectionSerializer
    queryset = Collection.objects

    def post(self, request, atr):
        serializer = self.serializer_class(data = {"name":request.data.get('name'), "schema":request.data.get('schema'), "artifact" : atr})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    def get(self, request, atr):
        serializer = self.serializer_class(self.queryset.filter(artifact = atr), many=True)
        return Response(serializer.data)
    
class CollectionSerializerDataAPI(APIView):
    permission_classes = [IsAuthenticated, IsVerified]
    def post(self, request, col):
        obj = Collection.objects.filter(id = col)[0]
        artifact = obj.artifact.id
        collection = obj.id
        # schema = obj.schema
        data = json.dumps(request.data)
        response = requests.post(f'http://localhost:8080/{artifact}/{collection}', data).json()
        return Response(response)
    def get(self, request, col):
        obj = Collection.objects.filter(id = col)[0]
        artifact = obj.artifact.id
        collection = obj.id
        response = requests.get(f'http://localhost:8080/{artifact}/{collection}').json()
        return Response(response)