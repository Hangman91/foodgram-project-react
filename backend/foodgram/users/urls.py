from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import FollowListViewSet

router = SimpleRouter()

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
