"""
============================================================
File Name: test_api.py
Brief Description:
Unit tests for the prototype REST API endpoints:
- GET /api/events/
- GET /api/events/<id>/

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                                  | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Added tests for event list and event detail API     | DEV-123
============================================================
"""

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from main.models import AccessibilityProfile
from main.test_suite.model_factories import EventFactory


class EventAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def _sensory_level_field_exists() -> bool:

        #Returns True if the AccessibilityProfile model includes a sensory_level field.
        #This keeps tests compatible if you remove that field later.

        try:
            AccessibilityProfile._meta.get_field("sensory_level")
            return True
        except Exception:
            return False

    def test_api_events_list_returns_published_events(self):
        # Arrange: create one published event (EventFactory will also create user/profile unless overridden)
        event = EventFactory(status="PUBLISHED")

        # Act
        response = self.client.get("/api/events/")

        # Assert
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        # Find our event in the response
        matching = [e for e in data if e.get("id") == event.id]
        self.assertEqual(len(matching), 1)

        event_json = matching[0]

        # Basic event keys (keep this lightweight)
        self.assertIn("title", event_json)
        self.assertIn("description", event_json)
        self.assertIn("start_datetime", event_json)
        self.assertIn("end_datetime", event_json)
        self.assertIn("accessibility_profile", event_json)

        # Nested accessibility profile keys
        ap = event_json["accessibility_profile"]
        self.assertIsInstance(ap, dict)
        self.assertIn("wheelchair_access", ap)
        self.assertIn("noise_level", ap)
        self.assertIn("lighting_conditions", ap)
        self.assertIn("crowd_level", ap)

        if self._sensory_level_field_exists():
            self.assertIn("sensory_level", ap)

    def test_api_event_detail_returns_single_event(self):
        # Arrange
        event = EventFactory(status="PUBLISHED")

        # Act
        response = self.client.get(f"/api/events/{event.id}/")

        # Assert
        self.assertEqual(response.status_code, 200)

        event_json = response.json()
        self.assertEqual(event_json["id"], event.id)
        self.assertEqual(event_json["title"], event.title)

        # Ensure nested profile exists and matches expected structure
        self.assertIn("accessibility_profile", event_json)
        ap = event_json["accessibility_profile"]
        self.assertIsInstance(ap, dict)

        # Confirm a couple of values match the actual linked profile
        self.assertEqual(ap["wheelchair_access"], event.accessibility_profile.wheelchair_access)
        self.assertEqual(ap["noise_level"], event.accessibility_profile.noise_level)

        if self._sensory_level_field_exists():
            self.assertEqual(ap["sensory_level"], event.accessibility_profile.sensory_level)

    def test_api_event_detail_404_when_missing(self):
        response = self.client.get("/api/events/999999/")
        self.assertEqual(response.status_code, 404)
