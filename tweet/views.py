from rest_framework.decorators import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.shortcuts import render

from tweet.serializers import TweetSerializer
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
