from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            # Проверяем количество открытых объявлений текущего пользователя.
            # Если создается новое объявление со статусом OPEN или
            # обновляется статус на OPEN, учитываем лимит.
            status = data.get("status", self.instance.status if self.instance else None)
            if status == "OPEN":
                count = Advertisement.objects.filter(
                    creator=request.user,
                    status="OPEN"
                ).count()
                # Если это обновление существующего OPEN объявления, вычтем его из счетчика
                if self.instance and self.instance.status == "OPEN":
                    count -= 1
                if count >= 10:
                    raise serializers.ValidationError(
                        "У пользователя уже есть 10 открытых объявлений."
                    )

        return data
