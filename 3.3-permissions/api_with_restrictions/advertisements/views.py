from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.serializers import AdvertisementSerializer


class IsAuthorOrAdmin(BasePermission):
    """Разрешение: только автор объявления или админ."""

    def has_permission(self, request, view):
        # Разрешаем доступ к методам чтения всем пользователям.
        if request.method in SAFE_METHODS:
            return True
        # Для write-операций требуется аутентификация.
        if request.method in ["DELETE"]:
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        # Админы могут удалять любые объявления.
        if request.user.is_staff:
            return True
        # Автор может удалять своё объявление.
        return obj.creator == request.user


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение: редактировать может только автор."""

    def has_permission(self, request, view):
        # Чтение доступно всем.
        if request.method in SAFE_METHODS:
            return True
        # Создание требует аутентификации.
        if request.method == "POST":
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        # Автор может обновлять и удалять своё объявление.
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthorOrReadOnly()]
        if self.action == "destroy":
            return [IsAuthorOrAdmin()]
        # Чтение (list, retrieve) доступно всем.
        return []
