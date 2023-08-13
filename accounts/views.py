from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import User
from .serializers import UserSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permisions import IsVerified
from django.http import HttpResponse
from rest_framework.response import Response
from .utils import sendVerificationMail, sendPasswordResetMail

# Create your views here.
class RegistrationAPI(GenericAPIView, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def post(self, request):
        return self.create(request)
    
class SendVerficationAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        try:
            sendVerificationMail(request)
            return Response({'status': 200,'message' : 'Please Check Your Mail, an Email verfication link has been provided'})
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class ValidateVerificationView(APIView):
    def get(self, request, id, token):
        try:
            user = User.objects.get(id = id)
            if(token == user.email_token):
                user.is_email_verified = True
                user.save()
                return HttpResponse('<h1>User is Verified Successfully</h1>')
            else:
                return HttpResponse('<h1>Token is not valid</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Sorry Some error has occured, error : {e}</h1>')

class PasswordResetAPI(APIView):
    def post(self, request):
        try:
            sendPasswordResetMail(request)
            return Response({'status': 200, 'message' : 'Please check your mail a password reset link has been provided'})
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class PasswordResetView(APIView):
    def get(self , request, id, token):
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            return render(request, "accounts/passwordreset.html", {'id' : id, 'token' : token})
        else:
            return HttpResponse('<h1>Token is not valid</h1>')
    def post(self, request, id, token):
        password = request.POST['password']
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            try:
                user_obj.set_password(password)
                user_obj.save()
                return HttpResponse('<h1>User Password changed Successfully</h1>')
            except Exception as e:
                return HttpResponse(f'<h1>Some error has occured, error : {e}</h1>')
        else:
            return HttpResponse('<h1>Token is not valid</h1>')