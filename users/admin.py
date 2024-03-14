from users.models import User, CarreraUser
from django.contrib import admin


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nit', 'first_name', 'username', 'email')
    search_fields = ('username', 'email', 'nit')
    fields = ('first_name', 'last_name', 'nit', 'email', 'type', 'avatar', 'password', 'is_active', 'carrera')
    exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined',)

@admin.register(CarreraUser)
class CarreraUserAdmin(admin.ModelAdmin):
    list_display = ('name',)
