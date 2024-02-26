from django import forms
from django.contrib import admin
from .models import Activity, Participation, User
from django.utils.translation import gettext_lazy as _

class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ActivityAdminForm, self).__init__(*args, **kwargs)
        # Filter the queryset for the 'teacher' field to only include users with type=='teacher'
        self.fields['teacher'].queryset = User.objects.filter(type='TEACHER')
