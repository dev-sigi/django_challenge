from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet

def all_tweet(request):
  tweets = Tweet.objects.all()
  return render(request, "all_tweet.html", {"tweets": tweets, "title": "All Tweets",},)
