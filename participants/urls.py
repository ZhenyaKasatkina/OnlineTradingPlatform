from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser

from participants.apps import ParticipantsConfig
from participants.permissions import IsActiveEmployee
from participants.views import (ParticipantCreateAPIView,
                                ParticipantDestroyAPIView,
                                ParticipantListAPIView,
                                ParticipantRetrieveAPIView,
                                ParticipantUpdateAPIView)

app_name = ParticipantsConfig.name


urlpatterns = [
    path(
        "create/",
        ParticipantCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="create",
    ),
    path(
        "",
        ParticipantListAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="list",
    ),
    path(
        "view/<int:pk>/",
        ParticipantRetrieveAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="view",
    ),
    path(
        "update/<int:pk>/",
        ParticipantUpdateAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="update",
    ),
    path(
        "delete/<int:pk>/",
        ParticipantDestroyAPIView.as_view(permission_classes=(IsAdminUser,)),
        name="delete",
    ),
]
