from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from django.shortcuts import render

from tweet.serializers import TweetListSerializer
from .models import Tweet


@api_view(["GET"])
def all_tweet(request):
  tweets = Tweet.objects.all()
  serializer = TweetListSerializer(tweets, many=True)
  return render(request,
                "all_tweet.html",
                {
                  "tweets": serializer.data,
                  "title": "All Tweets",
                },
              )
