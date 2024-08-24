from rest_framework.serializers import ModelSerializer

from users.models import User


class UserFullSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "last_name", "first_name", "password", "employer"]


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        read_only_fields = (
            "email",
            "last_name",
            "first_name",
        )
        fields = [
            "id",
            "email",
            "last_name",
            "first_name",
            "employer",
        ]
