from django.urls import path
from . import views

urlpatterns = [
    path("", views.TweetList.as_view(), name="all_tweet"),
    path("<int:pk>", views.TweetDetail.as_view(), name="tweet detail"),
]
