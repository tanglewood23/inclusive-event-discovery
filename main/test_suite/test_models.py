"""
============================================================
File Name: test_models.py
Brief Description:
Unit tests for core prototype models, validating system-derived
sensory_level behaviour and basic model representations.

Author: Gavin Plucknett
Created: 2026-01-01
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                                  | Reference
------------------------------------------------------------
v1.0    | 2026-01-01 | Tests for sensory derivation + model relationships  | DEV-124
============================================================
"""

from django.test import TestCase
from main.models import *

from main.test_suite.model_factories import (UserFactory, AccessibilityProfileFactory, EventFactory)

#Test Models Exist
class ModelsExist(TestCase):
    def test_AccessibilityProfile_Exists(self):
        self.assertTrue(AccessibilityProfile)
        self.assertTrue(isinstance(AccessibilityProfile, type))

    def test_Event_Exists(self):
        self.assertTrue(Event)
        self.assertTrue(isinstance(Event, type))

#Test model fields exist and are of right data type
class ModelFieldTests(TestCase):

    # Function to test if field exists
    def assert_field_exists(self, model_cls, field_name: str):
        try:
            model_cls._meta.get_field(field_name)
        except Exception as exc:
            self.fail(f"Expected field '{field_name}' on model '{model_cls.__name__}' but it was missing. Error: {exc}")

    # Function to test if field is correct data type
    def assert_field_is_instance(self, model_cls, field_name: str, field_type):
        field = model_cls._meta.get_field(field_name)
        self.assertIsInstance(
            field,
            field_type,
            msg=f"Field '{model_cls.__name__}.{field_name}' expected type {field_type} but got {type(field)}",
        )

    # ---- AccessibilityProfile fields ----
    def test_accessibility_profile_expected_fields_exist(self):
        expected_fields = [
            "wheelchair_access",
            "accessible_toilets",
            "quiet_space_available",
            "noise_level",
            "lighting_conditions",
            "crowd_level",
            "sensory_level",
            "additional_notes",
        ]

        for f in expected_fields:
            self.assert_field_exists(AccessibilityProfile, f)

    def test_accessibility_profile_field_types(self):
        self.assert_field_is_instance(AccessibilityProfile, "wheelchair_access", models.BooleanField)
        self.assert_field_is_instance(AccessibilityProfile, "accessible_toilets", models.BooleanField)
        self.assert_field_is_instance(AccessibilityProfile, "quiet_space_available", models.BooleanField)
        self.assert_field_is_instance(AccessibilityProfile, "noise_level", models.CharField)
        self.assert_field_is_instance(AccessibilityProfile, "lighting_conditions", models.CharField)
        self.assert_field_is_instance(AccessibilityProfile, "crowd_level", models.CharField)
        self.assert_field_is_instance(AccessibilityProfile, "sensory_level", models.CharField)
        self.assert_field_is_instance(AccessibilityProfile, "additional_notes", models.TextField)

    # ---- Event fields ----
    def test_event_expected_fields_exist(self):
        expected_fields = [
            "title",
            "description",
            "category",
            "age_min",
            "age_max",
            "start_datetime",
            "end_datetime",
            "location_text",
            "postcode",
            "price",
            "booking_required",
            "booking_url",
            "accessibility_profile",
            "created_by_user",
            "status",
            "created_at",
            "updated_at",
        ]

        for f in expected_fields:
            self.assert_field_exists(Event, f)

    def test_event_relationship_types(self):
        # One-to-one relationship to AccessibilityProfile
        self.assert_field_is_instance(Event, "accessibility_profile", models.OneToOneField)

        # created_by_user is usually a FK to auth.User
        self.assert_field_is_instance(Event, "created_by_user", models.ForeignKey)

    def test_event_field_types_basic(self):
        self.assert_field_is_instance(Event, "title", models.CharField)
        self.assert_field_is_instance(Event, "description", models.TextField)
        self.assert_field_is_instance(Event, "category", models.CharField)
        self.assert_field_is_instance(Event, "start_datetime", models.DateTimeField)
        self.assert_field_is_instance(Event, "end_datetime", models.DateTimeField)
        self.assert_field_is_instance(Event, "location_text", models.CharField)
        self.assert_field_is_instance(Event, "postcode", models.CharField)
        self.assert_field_is_instance(Event, "price", models.DecimalField)
        self.assert_field_is_instance(Event, "booking_required", models.BooleanField)
        self.assert_field_is_instance(Event, "booking_url", models.URLField)
        self.assert_field_is_instance(Event, "status", models.CharField)
        self.assert_field_is_instance(Event, "created_at", models.DateTimeField)
        self.assert_field_is_instance(Event, "updated_at", models.DateTimeField)
 
class AccessibilityProfileModelTests(TestCase):

    def test_str_returns_identifier(self):
        profile = AccessibilityProfileFactory()
        self.assertIn(f"#{profile.pk}", str(profile))


class EventModelTests(TestCase):
    def test_event_has_accessibility_profile(self):
        event = EventFactory()
        self.assertIsNotNone(event.accessibility_profile_id)
        self.assertEqual(event.accessibility_profile.event, event)

    def test_event_str_returns_title(self):
        event = EventFactory(title="My Event")
        self.assertEqual(str(event), "My Event")
