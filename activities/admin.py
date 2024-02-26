from django.contrib import admin

from .forms import ActivityAdminForm
from .models import *


@admin.register(Activity)
class ActivitiesAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    list_display = ('title', 'description')
    readonly_fields = ('qr_code', )
    exclude = ('students',)

@admin.register(PointsUser)
class PointsUserAdmin(admin.ModelAdmin):
    list_display = ('points','Nombre', 'nit')
    search_fields = ('user__nit','user__email')
    readonly_fields = ('points', 'Nombre', 'nit', 'user')

    def Nombre(self, obj):
        return obj.user.first_name
    def nit(self, obj):
        return obj.user.nit
