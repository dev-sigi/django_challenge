from rest_framework import serializers

from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class TiniUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            "user_id",
            "name",
        )