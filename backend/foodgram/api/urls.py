from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (FollowListViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

router = SimpleRouter()

router.register(
    'tags',
    TagViewSet
)
router.register(
    'recipes',
    RecipeViewSet
)
router.register(
    'ingredients',
    IngredientViewSet
)

router.register(
    'users/subscriptions',
    FollowListViewSet,
    basename='follows'
)
router.register(
    'users/(?P<users_id>[^/.]+)/subscribe',
    FollowListViewSet,
    basename='follows'
)


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
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
]
