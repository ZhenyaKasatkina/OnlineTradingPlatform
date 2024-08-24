from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from participants.models import Participant
from participants.serializers import (ParticipantsCreateSerializer,
                                      ParticipantsSerializer)


class ParticipantCreateAPIView(CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantsCreateSerializer


class ParticipantListAPIView(ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("country",)


class ParticipantRetrieveAPIView(RetrieveAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantsSerializer


class ParticipantUpdateAPIView(UpdateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantsSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(user__pk=self.request.user.pk)
            return queryset
        else:
            return None


class ParticipantDestroyAPIView(DestroyAPIView):
    queryset = Participant.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(email=self.request.user.email)
            return queryset
        else:
            return None
