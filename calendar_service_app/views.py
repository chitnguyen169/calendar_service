from datetime import datetime

import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from calendar_service_app.models import Event
from calendar_service_app.serializers import EventSerializer


class EventView(ViewSet):
    def create(self, request):
        """
        Method to create an event.
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            resp_data = {
                "id": event.id,
                "time": event.time,
                "description": event.description
            }
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request=None):
        """
        Method to list all events with filter by datetime.
        """
        datetime_format = request.query_params.get(
            "datetime_format", "%Y-%m-%dT%H:%M:%S"
        )
        from_datetime_str = request.query_params.get("from_datetime")
        to_datetime_str = request.query_params.get("to_datetime")

        # default value to today at 00:00:00 to now() if not in query param
        now = timezone.now()
        from_datetime = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        to_datetime = now

        if from_datetime_str:
            try:
                from_datetime = datetime.strptime(
                    from_datetime_str, datetime_format
                )
            except ValueError as e:
                return Response(
                    {"error": f"Invalid datetime format for from_datetime: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if to_datetime_str:
            try:
                to_datetime = datetime.strptime(
                    to_datetime_str, datetime_format
                )
            except ValueError as e:
                return Response(
                    {"error": f"Invalid datetime format for to_datetime: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Parse with tz info to filter to avoid warning
        tz_val = getattr(settings, 'TIME_ZONE', 'UTC')
        tz = pytz.timezone(tz_val)
        from_dt = from_datetime.replace(tzinfo=tz)
        to_dt = to_datetime.replace(tzinfo=tz)

        events = Event.objects.filter(time__range=(from_dt, to_dt))
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetailView(ViewSet):

    def list(self, request, id):
        """
        Method to list event by id.
        """
        datetime_format_param = request.query_params.get("datetime_format")
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise NotFound({"error": f"Event with id {id} not found."})

        serializer = EventSerializer(event)
        resp_data = serializer.data
        if datetime_format_param:
            formatted_dt = event.time.strftime(datetime_format_param)
            resp_data.update({"time": formatted_dt})

        return Response(resp_data, status=status.HTTP_200_OK)
