from django.contrib import admin
from .models import Tweet, Like


class ElonMuskFilter(admin.SimpleListFilter):

    title = "ElonMuskFilter"
    parameter_name = "elon_musk_filter"

    def lookups(self, request, model_admin):
        return (("Elon Musk", "Elon Musk"), ("Not Elon Musk", "Not Elon Musk"))

    def queryset(self, request, tweet):
        if self.value() == "Elon Musk":
            return tweet.filter(payload__contains="Elon Musk")
        if self.value() == "Not Elon Musk":
            return tweet.exclude(payload__contains="Elon Musk")

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "user__name",
                    "payload",
                    "created_at",
                    "updated_at",
                    "total_likes",)
    search_fields = ("user__name",
                     "payload", # Search by payload.
                    )
    list_filter = ("created_at", # Filter by create_at.
                   "updated_at",
                   ElonMuskFilter,
                  )

    def total_likes(self, tweet: Tweet):
        return tweet.likes.count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "user__name",
                    "tweet__payload",
                    "created_at",
                    "updated_at",
                    )
    search_fields = ("user__name", # Search by username of user foreign key.
                    )
    list_filter = ("created_at", # Filter by create_at
                   "updated_at",
                  )
