from rest_framework.throttling import SimpleRateThrottle


class AnonymousRateThrottle(SimpleRateThrottle):
    """Лимит для неавторизованных пользователей: 10 запросов в минуту."""

    scope = "anonymous"
    rate = "10/m"

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return self.get_ident(request)
        return None


class AuthenticatedRateThrottle(SimpleRateThrottle):
    """Лимит для авторизованных пользователей: 20 запросов в минуту."""

    scope = "authenticated"
    rate = "20/m"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"throttle_{request.user.id}"
        return None


class UserRateThrottle(SimpleRateThrottle):
    """Выбирает throttle в зависимости от аутентификации пользователя."""

    authenticated_throttle = AuthenticatedRateThrottle()
    anonymous_throttle = AnonymousRateThrottle()

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return self.authenticated_throttle.get_cache_key(request, view)
        return self.anonymous_throttle.get_cache_key(request, view)

    def allow_request(self, request, view):
        if request.user and request.user.is_authenticated:
            return self.authenticated_throttle.allow_request(request, view)
        return self.anonymous_throttle.allow_request(request, view)
