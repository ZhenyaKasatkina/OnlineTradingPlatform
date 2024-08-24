from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserUpdateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "create/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="create",
    ),
    path("", UserListAPIView.as_view(permission_classes=(IsAdminUser,)), name="list"),
    path(
        "update/<int:pk>/",
        UserUpdateAPIView.as_view(permission_classes=(IsAdminUser,)),
        name="update",
    ),
    path(
        "delete/<int:pk>/",
        UserDestroyAPIView.as_view(permission_classes=(IsAdminUser,)),
        name="delete",
    ),
]
