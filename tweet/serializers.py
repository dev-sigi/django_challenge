from rest_framework import serializers
from .models import Tweet


class TweetListSerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(required=True, max_length=180)
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_user(self, tweet):
        return {"user_id": tweet.user.user_id, "name": tweet.user.name}