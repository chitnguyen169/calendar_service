import django

django.setup()
from django.test import TestCase
from datetime import datetime
from calendar_service_app.models import Event


class EventModelTest(TestCase):
    def test_create_event(self):
        desc = "Test description"
        t = datetime(2024, 12, 14, 10, 0, 0)
        event = Event.objects.create(
            description=desc,
            time=t
        )
        self.assertEqual(event.description, desc)
        self.assertEqual(event.time, t)
        self.assertEqual(Event.objects.count(), 1)
