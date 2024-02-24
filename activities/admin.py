from django.contrib import admin
from .models import *


class ActivityScheduleInline(admin.TabularInline):
    model = ActivitySchedule
    extra = 1  #

@admin.register(Activity)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    exclude = ('students',)
    inlines = [ActivityScheduleInline]

