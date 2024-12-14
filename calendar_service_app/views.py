from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from calendar_service_app.models import Event
from calendar_service_app.serializers import EventSerializer


# Create your views here.
class EventView(APIView):

    def post(self, request):
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

    def get(self, request, id=None):
        if id:
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
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
