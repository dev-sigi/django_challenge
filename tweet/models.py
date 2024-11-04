from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):

    payload = models.TextField(max_length=180)
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="tweets")

    def __str__(self):
        return f"{self.user}님의 트윗: {self.payload}"

    class Meta:
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"


class Like(CommonModel):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user}님이 {self.tweet}를 좋아합니다."

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
