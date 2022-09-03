from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.mixins import ReadCreateViewSet
from .serializers import FollowListSerializer
from .models import Follow

User = get_user_model()


class FollowListViewSet(ReadCreateViewSet):

    serializer_class = FollowListSerializer

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):

        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        double_subscribe = Follow.objects.filter(
            user=request.user,
            following=user
        ).exists()

        if request.user.id == int(user_id):
            error = {'errors': 'Невозможно подписаться на самого себя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        elif double_subscribe:
            error = {'errors': 'Вы уже подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(
            user=request.user, following=user)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['users_id']
        subscribe_user = get_object_or_404(User, id=user_id)

        try:
            subscribe = Follow.objects.get(
                user=request.user,
                following=subscribe_user
            )
        except ObjectDoesNotExist:
            error = {'errors': 'Вы не подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
