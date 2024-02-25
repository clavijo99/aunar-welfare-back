from users.models import User
from django.contrib import admin


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'username', 'email')
    search_fields = ('username', 'email', 'id')
    fields = ('first_name', 'last_name', 'email', 'type', 'avatar', 'password')
    exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 'is_active')
