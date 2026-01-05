"""
============================================================
File Name: serializers.py
Brief Description:
Serializers for the prototype REST API. Provides read-only
serialization for Event and linked AccessibilityProfile.

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                     | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Initial serializers for Event API      | DEV-123
============================================================
"""

from rest_framework import serializers
from .models import Event, AccessibilityProfile

# AccessibilityProfile serializer format
class AccessibilityProfileSerializer(serializers.ModelSerializer):
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
            "sensory_level",       # remove if you deleted this field
            "additional_notes",
        ]
        read_only_fields = fields

#Event Serializer format
class EventSerializer(serializers.ModelSerializer):
    #Include accessibility data
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
