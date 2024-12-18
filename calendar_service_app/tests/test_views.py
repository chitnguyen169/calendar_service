from datetime import datetime
from unittest.mock import patch

import pytz
from rest_framework.test import APITestCase

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

    @patch("django.utils.timezone.now", return_value=datetime(2024, 12, 14, 20, 0, 0))
    def test_get_all_events_today(self, _):
        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_post_event(self):
        data = {"description": "New event", "time": "2024-12-14T12:00:00Z"}
        response = self.client.post("/events", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "New event")
        self.assertEqual(response.json()["time"], "2024-12-14T12:00:00Z")
        self.assertIsInstance(response.json()["id"], int)

    def test_cannot_get_events_with_datetime_filter(self):
        url = "/events?datetime_format=%Y-%m-%d&from_datetime=14-12-2024&to_datetime=2024-12-15"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid datetime format for from_datetime", response.data["error"])

    def test_get_events_with_datetime_filter_without_from_to_dt(self):
        url = "/events?datetime_format=%Y-%m-%d"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_events_with_datetime_filter(self):
        test_cases = (
            "/events?datetime_format=%Y-%m-%d&from_datetime=2024-12-14&to_datetime=2024-12-15",
            "/events?datetime_format=%d-%m-%Y&from_datetime=14-12-2024&to_datetime=15-12-2024",
            "/events?datetime_format=%Y-%m-%dT%H:%M:%SZ&from_datetime=2024-12-13T12:00:00Z"
            "&to_datetime=2024-12-14T23:00:00Z",
            "/events?from_datetime=2024-12-13T12:00:00&to_datetime=2024-12-14T15:00:00"

        )
        for case in test_cases:
            with self.subTest(case):
                response = self.client.get(case)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json()), 1)
                self.assertEqual(response.json()[0]["description"], "Event 1")

    @patch("django.utils.timezone.now", return_value=datetime(2024, 12, 15, 20, 0, 0))
    def test_get_events_without_from_datetime(self, _):
        url = "/events?datetime_format=%Y-%m-%dT%H:%M:%S&to_datetime=2024-12-15T15:00:00"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["description"], "Event 2")

    @patch("django.utils.timezone.now", return_value=datetime(2024, 12, 14, 20, 0, 0))
    def test_get_events_without_to_datetime(self, _):
        url = "/events?datetime_format=%Y-%m-%dT%H:%M:%S&from_datetime=2024-12-14T00:00:00"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["description"], "Event 1")

    @patch("django.utils.timezone.now", return_value=datetime(2024, 12, 15, 23, 0, 0))
    def test_get_events_without_from_to_datetime(self, _):
        url = "/events?datetime_format=%Y-%m-%d"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["description"], "Event 2")

    def test_cannot_get_event_by_id(self):
        url = f"/events/{self.event1.id + 1000}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_event_by_id(self):
        url = f"/events/{self.event1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_resp = {
            "description": "Event 1",
            "time": "2024-12-14T10:00:00",
            "id": self.event1.id
        }
        self.assertEqual(expected_resp, response.json())

    def test_get_event_by_id_with_dt_format(self):
        url = f"/events/{self.event1.id}?datetime_format=%d-%m"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_resp = {
            "description": "Event 1",
            "time": "14-12",
            "id": self.event1.id
        }
        self.assertEqual(expected_resp, response.json())

    def test_get_event_by_id_with_another_dt_format(self):
        url = f"/events/{self.event1.id}?datetime_format=%d-%m-%YT%H:%M"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_resp = {
            "description": "Event 1",
            "time": "14-12-2024T10:00",
            "id": self.event1.id
        }
        self.assertEqual(expected_resp, response.json())
