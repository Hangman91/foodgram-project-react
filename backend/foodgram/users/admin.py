from django.contrib import admin

from users.models import Follow, User


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


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following',
        'id'
    )
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
