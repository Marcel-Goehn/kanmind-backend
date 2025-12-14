from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer used to register a new user.

    This serializer ensures:
        - That the provided email address is unique and not in use
        - That the password and repeated password match
    """

    fullname = serializers.CharField(max_length=100, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "fullname", "email", "password", "repeated_password"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": { "required": True },
            "password": { "write_only": True },
            "username": { "required": False }
        }

    def validate_email(self, value):
        """Makes sure that the email is not already in use."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({ "error": "Email already in use!" })
        return value

    def validate(self, data):
        """Makes sure that both, the password and repeated password match."""

        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({ "error": "Passwords don't match!" })
        return data

    def create(self, validated_data):
        """
        This method does the following:
            - creates a new user instance
            - hashes the entered password
            - saves the new user to the database
            - returns the new instance
        """

        account = User(username=validated_data["fullname"], email=validated_data["email"])
        account.set_password(validated_data["password"])
        account.save()
        return account
    

class LoginSerializer(serializers.ModelSerializer):
    """Serializer used to login a registered user."""

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True}
        }

    def validate(self, data):
        """
        The validation methods makes sure:
            - that the entered email belongs to a already registered user
            - checks if the entered password matches the password in the database
        """

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({ "error": "Email does not exist!" })

        if not user.check_password(data["password"]):
            raise serializers.ValidationError({ "error": "Password does not match!" })
        
        data["user"] = user
        return data
        
        
