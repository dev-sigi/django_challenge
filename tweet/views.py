from rest_framework.decorators import APIView
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_204_NO_CONTENT,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tweet.serializers import TweetSerializer, TweetDetailSerializer
from .models import Tweet


class TweetList(APIView):

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )

    def post(self, request):
        try:
            user = request.user
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(
                    serializer.data,
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        except APIException as e:
            return Response(
                e.detail,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_tweet(self, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
            return tweet
        except Tweet.DoesNotExist:
            raise NotFound(detail=f"{pk}의 트윗이 존재하지 않습니다.")

    def get(self, request, pk):
        tweet = self.get_tweet(pk)
        try:
            serializer = TweetDetailSerializer(tweet)
            return Response(
                serializer.data,
                status=HTTP_200_OK,
            )
        except APIException as e:
            return Response(
                e.detail,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        tweet = self.get_tweet(pk)

        try:
            if request.user != tweet.user:
                raise PermissionDenied("트윗 수정은 본인만 가능합니다.")

            serializer = TweetDetailSerializer(
                tweet,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        except APIException as e:
            return Response(
                e.detail,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk):
        tweet = self.get_tweet(pk)

        try:
            if request.user != tweet.user:
                raise PermissionDenied("트윗 삭제는 본인만 가능합니다.")

            tweet.delete()

            return Response(
                status=HTTP_204_NO_CONTENT,
            )

        except APIException as e:
            return Response(e.detail, status=HTTP_500_INTERNAL_SERVER_ERROR)
