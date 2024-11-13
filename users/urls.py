from django.urls import path
from . import views

urlpatterns = [
    path("", views.User.as_view(), name="all_user"),
    path("<int:user_id>", views.UserDetail.as_view(), name="user_detail"),
    path("<int:user_id>/tweets", views.UserTweetList.as_view(), name="user_tweets"),
    path("password", views.ChangePassword.as_view(), name="change_password"),
    path("login", views.LogIn.as_view(), name="login"),
    path("logout", views.LogOut.as_view(), name="logout"),
]
