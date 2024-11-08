from django.urls import path
from . import views

urlpatterns = [
  path("", views.TweetList.as_view(), name="all_tweet"),
]
