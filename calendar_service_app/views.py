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


class EventListView(ViewSet):
    def create(self, request):
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
        datetime_format = request.query_params.get("datetime_format", "%Y-%m-%dT%H:%M:%S")
        from_datetime_str = request.query_params.get("from_datetime")
        to_datetime_str = request.query_params.get("to_datetime")
        if request.query_params and datetime_format:
            try:
                now = timezone.now()
                default_from_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
                from_datetime = (
                    datetime.strptime(from_datetime_str, datetime_format)
                    if from_datetime_str
                    else default_from_datetime
                )
                tz_val = getattr(settings, 'TIME_ZONE', 'UTC')
                print(tz_val)
                tz = pytz.timezone(tz_val)
                from_dt = from_datetime.replace(tzinfo=tz)

                to_datetime = (
                    datetime.strptime(to_datetime_str, datetime_format)
                    if to_datetime_str
                    else now
                )
                to_dt = to_datetime.replace(tzinfo=tz)
            except ValueError as e:
                return Response(
                    {"error": f"Invalid datetime format or value: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            events = Event.objects.filter(time__range=(from_dt, to_dt))
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Create your views here.
class EventDetailView(ViewSet):

    def list(self, request, id):
        datetime_format_param = request.query_params.get("datetime_format", None)
        try:
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
        except Event.DoesNotExist:
            raise NotFound({"error": f"Event with id {id} not found."})

        resp_data = {
            "id": event.id,
            "description": event.description
        }
        dt = event.time
        original_format = "%Y-%m-%d %H:%M:%S%z"
        original_dt = datetime.strptime(str(dt), original_format)
        if datetime_format_param:
            formatted_dt = original_dt.strftime(datetime_format_param)
            resp_data.update({"time": formatted_dt})

            return Response(resp_data, status=status.HTTP_200_OK)
        formatted_dt = original_dt.strftime("%Y-%m-%dT%H:%M:%S")
        resp_data.update({"time": formatted_dt})
        return Response(resp_data, status=status.HTTP_200_OK)
