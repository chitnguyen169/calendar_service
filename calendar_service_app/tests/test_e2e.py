from datetime import datetime, timezone
from unittest.mock import patch

from rest_framework.test import APITestCase


class E2ETest(APITestCase):
    def test_e2e_function(self):
        # Create a new event
        event1 = self.client.post("/events", {"description": "Event 1",
                                              "time": "2024-12-14T10:00:00Z"}
        )
        self.assertEqual(event1.status_code, 201)

        # Create another new event
        event2 = self.client.post("/events", {"description": "Event 2",
                                              "time": "2024-12-15T20:00:00Z"})
        self.assertEqual(event2.status_code, 201)

        # Retrieve the event by ID
        event1_id = event1.json()["id"]
        response = self.client.get(f"/events/{event1_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Event 1")
        self.assertEqual(response.data["time"], "2024-12-14T10:00:00")

        # Retrieve the event by ID with datetime_format
        event2_id = event2.json()["id"]
        response = self.client.get(
            f"/events/{event2_id}?datetime_format=%d-%m-%Y")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Event 2")
        self.assertEqual(response.data["time"], "15-12-2024")

        # Retrieve the list of events
        fixed_time = datetime(2024, 12, 15, 21, 0, 0, tzinfo=timezone.utc)
        with patch('django.utils.timezone.now', return_value=fixed_time):
            response = self.client.get("/events")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], event2_id)

        # Retrieve the event with date range
        response = self.client.get(
            f"/events?datetime_format=%Y-%m-%d&from_datetime=2024-12-14"
            f"&to_datetime=2024-12-15")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Event 1")
        self.assertEqual(response.data[0]["time"], "2024-12-14T10:00:00")
        self.assertEqual(response.data[0]["id"], event1_id)
