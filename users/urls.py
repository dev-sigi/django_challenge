from django.urls import path
from . import views

urlpatterns = [
  path("<int:user_id>/tweets", views.UserTweetList.as_view(), name="user_tweets"),
]