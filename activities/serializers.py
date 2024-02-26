from rest_framework import serializers
from activities.models import *


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityRegisterUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
