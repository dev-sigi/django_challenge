from rest_framework import serializers

from .models import Users


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )


class TiniUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            "user_id",
            "name",
            "email",
        )
