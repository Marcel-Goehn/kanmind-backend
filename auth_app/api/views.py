from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
        

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = RegistrationSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "fullname": req.data["fullname"],
                "email": user.email,
                "user_id": user.pk
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = LoginSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.pk
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
