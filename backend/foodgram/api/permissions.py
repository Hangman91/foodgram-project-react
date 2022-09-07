from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """пермиссион для вью функций для рецептов"""

    def has_permission(self, request, view):
        """Доступ только аутентифицированному юзверю"""

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, views, obj):
        """Если добрались до объекта, то работает с ним только автор"""

        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
