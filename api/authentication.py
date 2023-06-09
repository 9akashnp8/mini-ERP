from rest_framework.authentication import TokenAuthentication as BaseAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


class TokenAuthentication(BaseAuthToken):
    keyword = "Bearer"


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """
    custom TokenRefreshSerializer that allows validation of
    refresh token from secure cookie.
    """

    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            return super().validate(attrs)
        raise InvalidToken("No valid token found in cookie")


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    custom TokenObtainPairView that, post login, sets refresh token
    as a secure cookie instead of sending as json response, sends access
    token in json response.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 Days, change to SIMPLE_JWT setting
            response.set_cookie(
                "refresh",
                response.data.get("refresh"),
                max_age=cookie_max_age,
                httponly=True,
                samesite="Lax",
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    custom TokenRefreshView that set's new refresh token
    as secure cookie provided a valid refresh token.
    """

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # 14 Days, change to SIMPLE_JWT setting
            response.set_cookie(
                "refresh",
                response.data.get("refresh"),
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)
