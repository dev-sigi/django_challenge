from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("user", "user__name","payload", "created_at", "updated_at", "total_likes",)
    search_fields = ("user__name",)
    list_filter = ("created_at", "updated_at",)

    def total_likes(self, tweet: Tweet):
        return tweet.likes.count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "user__name", "tweet__payload", "created_at", "updated_at",)
    search_fields = ("user__name",)
    list_filter = ("created_at", "updated_at",)
