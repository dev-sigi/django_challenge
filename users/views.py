from django.db import transaction

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import NotFound, APIException, ParseError

from tweet.serializers import TweetSerializer
from .serializers import TiniUserSerializer, PrivateUserSerializer

from .models import Users


# GET /users
class User(APIView):

    def get(self, request):
        users = Users.objects.all()
        serializer = TiniUserSerializer(
            users,
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        password = request.data.get("password")

        # 비밀번호 존재 여부 확인
        if password is None:
            raise ParseError("비밀번호가 존재하지 않습니다.")

        try:
            password = str(password)
        except Exception:
            raise ParseError("비밀번호를 문자열로 변환할 수 없습니다.")

        serializer = PrivateUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = serializer.save()
                user.set_password(password)
                user.save()

                return Response(PrivateUserSerializer(user).data, status=HTTP_200_OK)
        except Exception as e:
            raise APIException(f"사용자 생성 중 오류가 발생했습니다: {str(e)}")


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
