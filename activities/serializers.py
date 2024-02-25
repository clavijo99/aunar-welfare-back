from rest_framework import serializers
from activities.models import *


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'

class ActivityScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySchedule
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    activities_schedule = ActivityScheduleSerializer(many=True)
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityRegisterUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
