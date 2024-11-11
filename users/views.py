from rest_framework.decorators import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import render

from tweet.serializers import TweetSerializer
from .models import Users


class UserTweetList(APIView):

    def get(self, request, user_id):

        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return render(request, "user_not_found.html")

        tweets = user.tweets.all()
        serializer = TweetSerializer(tweets, many=True)

        return render(
            request,
            "user_tweets.html",
            {
                "tweets": serializer.data,
                "user": user,
                "title": f"{user.name}'s Tweets",
            },
        )
