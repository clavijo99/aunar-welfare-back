from django.contrib import admin
from .models import *


class ActivityScheduleInline(admin.TabularInline):
    model = ActivitySchedule
    extra = 1  #
    min_num = 1

@admin.register(Activity)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    readonly_fields = ('qr_code', )
    exclude = ('students',)
    inlines = [ActivityScheduleInline]

