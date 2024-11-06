from django.urls import path
from . import views

urlpatterns = [
  path("", views.all_tweet, name="all_tweet"),
]