from rest_framework.test import APITestCase
from tweet.models import Tweet
from users.models import Users


class TweetTestCase(APITestCase):

    USER_EMAIL = "test@test.com"
    USER_NAME = "test"
    USER_PASSWORD = "test1234!"
    PAYLOAD = "test payload"
    URL = "/api/v1/tweets/"

    def setUp(self):

        # 유저 생성
        user = Users.objects.create_user(
            email=self.USER_EMAIL,
            name=self.USER_NAME,
        )
        user.set_password(self.USER_PASSWORD)
        user.save()
        self.user = user

        # 트윗 생성
        Tweet.objects.create(
            payload=self.PAYLOAD,
            user=user,
        )

    def test_get_all_tweets(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "status code가 200이 아닙니다.")

        data = response.json()

        self.assertNotEqual(data[0]["created_at"], None, "created_at이 없습니다.")
        self.assertNotEqual(data[0]["updated_at"], None, "updated_at이 없습니다.")
        self.assertNotEqual(data[0]["user"], None, "user가 없습니다.")
        self.assertNotEqual(len(data), 0, "데이터가 없습니다.")

        self.assertEqual(len(data), 1, "데이터의 개수가 1개가 아닙니다.")
        self.assertEqual(data[0]["payload"], self.PAYLOAD, "payload가 다릅니다.")
        self.assertEqual(
            data[0]["user"]["user_id"], self.user.user_id, "user가 다릅니다."
        )

    def test_post_tweet(self):

        new_payload = "new payload"

        response = self.client.post(self.URL, data={"payload": new_payload})
        self.assertEqual(response.status_code, 403, "권한이 없습니다.")

        self.client.force_login(user=self.user)
        response = self.client.post(self.URL, data={"payload": new_payload})
        self.assertEqual(response.status_code, 201, "status code가 201이 아닙니다.")

        tweet_pk = response.json()["pk"]
        tweet = Tweet.objects.get(pk=tweet_pk)

        self.assertEqual(tweet.payload, new_payload, "payload가 다릅니다.")
        self.assertEqual(tweet.user, self.user, "user가 다릅니다.")
