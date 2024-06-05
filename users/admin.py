from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import FriendRequest, Profile

# Register your models here.


class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest
    search_fields = ('from_user',)
    ordering = ('from_user',)
    list_display = ('from_user', 'to_user', 'status', 'created')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_friends')

    def display_friends(self, obj):
        return ", ".join([friend.user.username for friend in obj.friends.all()])
    display_friends.short_description = 'Friends'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)