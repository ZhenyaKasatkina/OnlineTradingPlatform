from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView,
                                     get_object_or_404)

from participants.models import Participant
from users.models import User
from users.serializers import UserFullSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserFullSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        if Participant.objects.filter(email=user.email).exists():
            user.is_staff = True
            user.employer = get_object_or_404(Participant, email=user.email)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(employer=self.request.user.employer)
            return queryset
        else:
            return None


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(employer=None)
            return queryset
        else:
            return None


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(employer=self.request.user.employer)
            return queryset
        else:
            return None
