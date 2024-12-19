from datetime import datetime, timezone

from rest_framework.test import APITestCase

from calendar_service_app.serializers import EventSerializer


class EventSerializerTest(APITestCase):
    def test_valid_serialization(self):
        desc = "Test event"
        t = "2024-12-14T10:00:00Z"
        data = {
            "description": desc,
            "time": t
        }
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['description'], desc)
        self.assertEqual(serializer.validated_data['time'],
                         datetime(2024, 12, 14, 10, 0, 0, tzinfo=timezone.utc))

    def test_invalid_serialization(self):
        data = {"description": "Test event"}
        serializer = EventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('time', serializer.errors)

        data = {"time": "2024-12-14T10:00:00Z"}
        serializer = EventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
