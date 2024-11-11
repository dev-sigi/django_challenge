from rest_framework import serializers

from .models import Users


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class TiniUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            "user_id",
            "name",
            "email",
        )
