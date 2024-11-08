from rest_framework import serializers
from .models import Tweet

class TweetListSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = ["pk",
                  "payload",
                  "user",
                  "created_at",
                  "updated_at"]

    def get_user(self, tweet):
        return {"user_id": tweet.user.user_id, "name": tweet.user.name}

