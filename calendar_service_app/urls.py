from django.urls import path, include
from rest_framework.routers import DefaultRouter

from calendar_service_app.views import EventDetailView, EventView


router = DefaultRouter(trailing_slash=False)

router.register(r'events', EventView, basename="event")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:id>', EventDetailView.as_view(({'get': 'list'}), name="event-detail"))
]
