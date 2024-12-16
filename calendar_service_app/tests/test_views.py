import django

django.setup()
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime
import pytz

from calendar_service_app.models import Event


class EventViewTest(APITestCase):
    def setUp(self):
        self.event1 = Event.objects.create(
            description="Event 1", 
            time=datetime(2024, 12, 14, 10, 0, 0, tzinfo=pytz.UTC)
        )
        self.event2 = Event.objects.create(
            description="Event 2", 
            time=datetime(2024, 12, 15, 10, 0, 0, tzinfo=pytz.UTC)
        )

    def test_get_all_event(self):
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_post_event(self):
        data = {"description": "New event", "time": "2024-12-14T12:00:00Z"}
        response = self.client.post("/events/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['description'], "New event")
        self.assertEqual(response.json()['time'], "2024-12-14T12:00:00Z")
        self.assertIsInstance(response.json()['id'], int)

    def test_cannot_get_entries_with_datetime_filter(self):
        url = '/events?datetime_format=%Y-%m-%d&from_datetime=14-12-2024&to_datetime=2024-12-15'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid datetime format or value", response.data["error"])

    def test_get_entries_with_datetime_filter_without_from_to_dt(self):
        url = '/events?datetime_format=%Y-%m-%d'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_entries_with_datetime_filter(self):
        test_cases = (
            '/events?datetime_format=%Y-%m-%d&from_datetime=2024-12-14&to_datetime=2024-12-15',
            '/events?datetime_format=%d-%m-%Y&from_datetime=14-12-2024&to_datetime=15-12-2024',
            '/events?datetime_format=%Y-%m-%dT%H:%M:%SZ&from_datetime=2024-12-13T12:00:00Z'
            '&to_datetime=2024-12-14T23:00:00Z',

        )
        for case in test_cases:
            with self.subTest(case):
                response = self.client.get(case)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json()), 1)
                self.assertEqual(response.json()[0]['description'], "Event 1")
