from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from calendar_service_app.models import Event
from calendar_service_app.serializers import EventSerializer


# Create your views here.
class EventView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

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