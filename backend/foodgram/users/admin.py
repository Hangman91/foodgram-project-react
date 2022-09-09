from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from django.contrib.auth.models import Group
from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'id',
    )
    search_fields = ('username',)
    list_filter = ('email', 'first_name', 'last_name', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following',
        'id'
    )
    search_fields = ('user',)


class TokenAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False


admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
