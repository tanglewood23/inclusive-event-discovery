"""
============================================================
File Name: serializers.py
Brief Description:
Serializers for the prototype REST API. Provides read-only
serialization for Event and linked AccessibilityProfile.

Author: Gavin Plucknett
Updated: 2026-01-05
Current Version: v2.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                          | Reference
------------------------------------------------------------
v2.0    | 2026-01-05 | Nested LookupOption output (code/label)     | DEV-142
============================================================
"""

from rest_framework import serializers
from .models import Event, AccessibilityProfile, LookupOption, SensoryCategory


class SensoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SensoryCategory
        fields = ["code", "label"]
        read_only_fields = fields


class LookupOptionSerializer(serializers.ModelSerializer):
    category = SensoryCategorySerializer(read_only=True)

    class Meta:
        model = LookupOption
        fields = ["code", "label", "category"]
        read_only_fields = fields


class AccessibilityProfileSerializer(serializers.ModelSerializer):
    noise_level = LookupOptionSerializer(read_only=True)
    lighting_conditions = LookupOptionSerializer(read_only=True)
    crowd_level = LookupOptionSerializer(read_only=True)
    sensory_level = LookupOptionSerializer(read_only=True)

    class Meta:
        model = AccessibilityProfile
        fields = [
            "id",
            "wheelchair_access",
            "accessible_toilets",
            "quiet_space_available",
            "noise_level",
            "lighting_conditions",
            "crowd_level",
            "sensory_level",
            "additional_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class EventSerializer(serializers.ModelSerializer):
    category = LookupOptionSerializer(read_only=True)
    accessibility_profile = AccessibilityProfileSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
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
            "status",
            "created_at",
            "updated_at",
            "accessibility_profile",
        ]
        read_only_fields = fields
