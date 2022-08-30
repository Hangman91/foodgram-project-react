from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Юзернейм',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=True
    )
    is_subscribed = models.BooleanField('Подписка', default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Follow(models.Model):
    """Модель для подписок.
    Присутствует подписчик и на кого подписываются."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            )
        ]
    def __str__(self):
        return f'{self.user.username} - {self.following.username}'