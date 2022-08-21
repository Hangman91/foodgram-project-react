from django.urls import include, path

from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import SimpleRouter
from .views import TagViewSet, RecipeViewSet

router = SimpleRouter()

router.register(
    'tags',
    TagViewSet
)
router.register(
    'recipes',
    RecipeViewSet
)

urlpatterns = [
    path(
        '',
        include('djoser.urls')
    ),
    path(
        r'auth/',
        include('djoser.urls')
    ),
    path(
        r'auth/',
        include('djoser.urls.authtoken')
    ),
    path(
        '',
        include(router.urls)
    )
]

