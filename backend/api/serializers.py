from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatSession

class RepositorySerializer(serializers.Serializer):
    url = serializers.URLField()

class ChatSerializer(serializers.Serializer):

    repository = serializers.CharField()

    question = serializers.CharField()

    session_id = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    


class RegisterSerializer(serializers.ModelSerializer):

    password=serializers.CharField(write_only=True)

    class Meta:

        model=User

        fields=[
            "username",
            "email",
            "password"
        ]

    def create(self,validated_data):

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
    


class ChatSessionSerializer(serializers.ModelSerializer):

    repository = serializers.CharField(
        source="repository.name"
    )

    class Meta:

        model = ChatSession

        fields = [
            "id",
            "title",
            "repository",
            "created_at"
        ]