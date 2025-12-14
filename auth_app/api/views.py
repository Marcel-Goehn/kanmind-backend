from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
        

class RegistrationView(APIView):
    """Register a new user."""

    permission_classes = [AllowAny]

    def post(self, req):
        """
        This method does the following:
            - calls the validation methods in the serializer
            - saves the new user to the database
            - crates a token and associates it with the user
            - sends back a json response

        The response includes the following:
            - 200 OK if the request was a success
            - 400 if it was a bad request
        """
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
    """Login for a registered user."""

    permission_classes = [AllowAny]

    def post(self, req):
        """
        This method does the following:
            - calls the validation methods in the serializer
            - gives back a token to authenticate the user
            - sends back a json response

        The response includes the following:
            - 200 OK if the the email and password are correct
            - 400 if either/both the email and/or password are incorrect
        """
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
