from rest_framework import serializers

from users.serializers import TiniUserSerializer
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):

    user = TiniUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "pk",
            "payload",
            "user",
            "created_at",
            "updated_at",
        ]


class TweetDetailSerializer(serializers.ModelSerializer):

    user = TiniUserSerializer()

    class Meta:
        model = Tweet
        fields = (
            "id",
            "user",
            "payload",
            "created_at",
            "updated_at",
        )
