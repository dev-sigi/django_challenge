from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from django.shortcuts import render

from tweet.serializers import TweetListSerializer
from .models import Users


@api_view(["GET"])
def user_tweets(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return render(request, "user_not_found.html")

    if request.method == "GET":
        tweets = user.tweets.all()
        serializer = TweetListSerializer(tweets, many=True)
        return render(request,
                      "user_tweets.html",
                      {
                          "tweets": serializer.data,
                          "user": user,
                          "title": f"{user.name}'s Tweets",
                      },
                    )
