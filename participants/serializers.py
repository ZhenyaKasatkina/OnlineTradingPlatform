from rest_framework import serializers

from participants.models import Participant


class ParticipantsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house",
            "unit_name",
        ]


class ParticipantsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        if attrs["unit_name"] == "завод":
            if attrs["level"] != "0":
                raise serializers.ValidationError(
                    "Завод всегда находится на нулевом(0) уровне."
                )

        if attrs["unit_name"] in ["розничная сеть", "ИП"] and attrs["level"] not in [
            "1",
            "2",
        ]:
            raise serializers.ValidationError(
                "'Розничная сеть' и 'ИП' могут быть только на 1-м или 2-м уровне."
            )

        if attrs["supplier"]:
            if attrs["level"] not in ["2", "1"]:
                raise serializers.ValidationError(
                    "Если есть поставщик то Ваш уровень должен быть '1' или '2'."
                )
            if attrs["email"] == attrs["supplier"].email:
                raise serializers.ValidationError(
                    "Покупатель и поставщик не могут быть одним лицом."
                )
            if attrs["supplier"].level == "0" and attrs["level"] in ["0", "2"]:
                raise serializers.ValidationError(
                    "Вы выбрали поставщика с уровнем '0', Ваш уровень должен быть '1'."
                )
            if attrs["supplier"].level == "1" and attrs["level"] in ["0", "1"]:
                raise serializers.ValidationError(
                    "Вы выбрали поставщика с уровнем '1', Ваш уровень должен быть '2'."
                )
            if attrs["supplier"].level == "2":
                raise serializers.ValidationError(
                    "Поставщик с уровнем '2' не осуществляет поставки."
                )
        return attrs

    class Meta:
        model = Participant
        read_only_fields = ("debt",)
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house",
            "unit_name",
            "level",
            "supplier",
            "debt",
        ]
