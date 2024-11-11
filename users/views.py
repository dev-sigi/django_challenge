from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.exceptions import NotFound, APIException

from tweet.serializers import TweetSerializer
from .serializers import TiniUserSerializer

from .models import Users


# GET /users
class UserList(APIView):

    def get(self, request):
        users = Users.objects.all()
        serializer = TiniUserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


# GET /users/<int:user_id>
class UserDetail(APIView):

    def get_user(self, user_id):
        try:
            user = Users.objects.get(user_id=user_id)
            return user
        except Users.DoesNotExist:
            return NotFound(f"{user_id}에 해당하는 유저를 찾을 수 없습니다.")

    def get(self, request, user_id):
        user = self.get_user(user_id)
        try:
            serializer = TiniUserSerializer(user)
            return Response(
                serializer.data,
                status=HTTP_200_OK,
            )
        except APIException as e:
            return Response(
                e.detail,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


# GET /users/<int:user_id>/tweets
class UserTweetList(APIView):

    def get(self, request, user_id):

        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return NotFound(f"{user_id}에 해당하는 유저를 찾을 수 없습니다.")

        tweets = user.tweets.all()
        serializer = TweetSerializer(
            tweets,
            many=True,
        )

        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )
