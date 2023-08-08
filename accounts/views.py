from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import User
from .serializers import UserSerializer
from rest_framework.mixins import CreateModelMixin

# Create your views here.
class RegistrationAPI(GenericAPIView, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def post(self, request):
        return self.create(request)