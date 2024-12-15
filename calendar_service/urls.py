"""
URL configuration for calendar_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from calendar_service_app.views import EventDetailView, EventListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calendar_service_app.urls')),  # Include the app URLs at /api/
]

from django.contrib import admin
# from django.urls import path, include
# import urls as app_urls
# from calendar_service_app.views import EventListView
#
# urlpatterns = [
#     path('events/', EventListView.as_view(), name='event-list'),  # Event List View at /api/events/
# ]