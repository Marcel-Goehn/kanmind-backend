from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(max_length=100, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "fullname", "email", "password", "repeated_password"]
        extra_kwargs = {
            "id": { "read_only": True },
            "email": { "required": True },
            "password": { "write_only": True },
            "username": { "required": False }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({ "error": "Email already in use!" })
        return value

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({ "error": "Passwords don't match!" })
        return data

    def create(self, validated_data):
        account = User(username=validated_data["fullname"], email=validated_data["email"])
        account.set_password(validated_data["password"])
        account.save()
        return account