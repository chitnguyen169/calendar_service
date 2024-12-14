from rest_framework import serializers

from calendar_service_app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["description", "time", "id"]
