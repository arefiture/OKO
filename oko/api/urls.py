from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

APP_VERSION = 'v1'

app_name = 'api'


def add_version_url(url: str) -> str:
    """Добавляем версию к адресу и возвращаем полученный url."""
    return f'{APP_VERSION}/{url}'


urlpatterns = [
    # TODO: Добавить /register/ и /sign-out/
    path(
        add_version_url('auth/token/'), TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        add_version_url('auth/token/refresh/'), TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        add_version_url('auth/token/verify/'), TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
