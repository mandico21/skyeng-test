from django.contrib import admin

from users.models import UserABC


@admin.register(UserABC)
class UserAdmin(admin.ModelAdmin):
    ...
