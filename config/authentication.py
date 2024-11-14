from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import Users


class UsernameAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request.headers.get("X-USERNAME")
        if not email:
            return None

        try:
            user = Users.objects.get(email=email)
            return (user, None)
        except Users.DoesNotExist:
            raise AuthenticationFailed("사용자를 찾을 수 없습니다.")
