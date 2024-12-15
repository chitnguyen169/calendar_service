# from django.urls import path, include
# from django.contrib import admin
# from rest_framework.routers import DefaultRouter
#
# from calendar_service_app.views import (
#     EventListView, EventDetailView
# )
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from calendar_service_app.views import EventDetailView, EventListView
router = DefaultRouter()

# urlpatterns = [
#     path('events/', EventListView.as_view(), base='event-list'),
#     path('events/<int:id>/', EventDetailView.as_view(), name='event-detail'),
# ]
# define the router path and viewset to be used
router.register(r'events', EventListView, basename="event-list")
# router.register(r'events/<int:id>/', EventDetailView, basename="event-detail")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:id>/', EventDetailView.as_view(({'get': 'list'}), name="event-detail"))
]