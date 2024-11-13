from django.db import transaction
from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.exceptions import (
    NotFound,
    APIException,
    ParseError,
    AuthenticationFailed,
)

from tweet.serializers import TweetSerializer
from .serializers import TiniUserSerializer, PrivateUserSerializer

from rest_framework.permissions import IsAuthenticated

from common.utils import to_string
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

        password = to_string(password)

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


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def get_user(self, email):
        try:
            user = Users.objects.get(email=email)
            return user
        except Users.DoesNotExist:
            return NotFound(f"{email}에 해당하는 유저를 찾을 수 없습니다.")

    def put(self, request):

        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        user = self.get_user(email)

        if user != request.user:
            raise AuthenticationFailed("본인의 요청이 아닙니다.")

        if not old_password or not new_password:
            raise ParseError("비밀번호가 존재하지 않습니다.")

        old_password = to_string(old_password)
        new_password = to_string(new_password)

        if old_password == new_password:
            raise ParseError("기존 비밀번호와 동일한 비밀번호로 변경할 수 없습니다.")

        if not user.check_password(old_password):
            raise ParseError("기존 비밀번호가 일치하지 않습니다.")

        try:
            with transaction.atomic():
                user.set_password(new_password)
                user.save()

                return Response(status=HTTP_200_OK)
        except Exception as e:
            raise APIException(f"비밀번호 변경 중 오류가 발생했습니다: {str(e)}")


class LogIn(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise ParseError("아이디 또는 비밀번호를 입력하지 않았습니다.")

        email = to_string(email)
        password = to_string(password)

        try:
            user = authenticate(
                request,
                email=email,
                password=password,
            )
        except Exception as e:
            raise APIException(f"사용자 인증에 실패했습니다.: {str(e)}")

        if not user:
            return Response(
                "아이디 또는 비밀번호가 올바르지 않습니다.",
                status=HTTP_401_UNAUTHORIZED,
            )

        try:
            login(request, user)
        except Exception as e:
            raise APIException(f"로그인 중 오류가 발생했습니다.: {str(e)}")

        return Response(status=HTTP_200_OK)


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response(status=HTTP_200_OK)
        except Exception as e:
            raise APIException(f"로그아웃 중 오류가 발생했습니다.: {str(e)}")
