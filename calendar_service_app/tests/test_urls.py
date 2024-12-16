import django

django.setup()
from django.test import SimpleTestCase
from django.urls import resolve

from calendar_service_app.views import EventView, EventDetailView


class URLTest(SimpleTestCase):
    def test_event_list_url(self):
        url = "/events"
        self.assertEqual(resolve(url).func.cls, EventView)

    def test_event_detail_url(self):
        url = "/events/1"
        self.assertEqual(resolve(url).func.cls, EventDetailView)

