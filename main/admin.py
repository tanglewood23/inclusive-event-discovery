"""
============================================================
File Name: admin.py
Brief Description:
Registers core prototype models (Event, EventAccessibilityProfile)
with the Django admin for rapid prototyping.

Author: Gavin Plucknett
Created: 2026-01-06
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                       | Reference
------------------------------------------------------------
v1.0    | 2026-01-06 | Admin registration for prototype models  | DEV-118
============================================================
"""

from django.contrib import admin
from .models import *
from .forms import LookupOptionAdminForm


# ---------------------------
# SensoryCategory
# ---------------------------
@admin.register(SensoryCategory)
class SensoryCategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "code", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "code", "description")
    ordering = ("display_order", "label")


@admin.register(LookupOption)
class LookupOptionAdmin(admin.ModelAdmin):
    form = LookupOptionAdminForm

    list_display = ("option_type", "label", "code", "category", "display_order", "is_active")
    list_filter = ("option_type", "category", "is_active")
    search_fields = ("label", "code", "description")
    ordering = ("option_type", "category__display_order", "display_order", "label")

    autocomplete_fields = ("category",)

    fields = (
        "option_type",
        "code",
        "label",
        "description",
        "category",          # <- assign SensoryCategory at creation
        "display_order",
        "is_active",
    )


@admin.register(AccessibilityProfile)
class AccessibilityProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "wheelchair_access",
        "accessible_toilets",
        "quiet_space_available",
        "sensory_level",
        "noise_level",
        "lighting_conditions",
        "crowd_level",
        "updated_at",
    )
    list_filter = (
        "wheelchair_access",
        "accessible_toilets",
        "quiet_space_available",
        "sensory_level",
        "noise_level",
        "lighting_conditions",
        "crowd_level",
    )
    search_fields = ("additional_notes",)
    ordering = ("-updated_at",)

    autocomplete_fields = (
        "noise_level",
        "lighting_conditions",
        "crowd_level",
        "sensory_level",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category",  "start_datetime", "end_datetime")
    list_filter = ("status", "category")
    search_fields = ("title", "description", "location_text", "postcode")
    ordering = ("start_datetime",)

    autocomplete_fields = ("category", "accessibility_profile", "created_by_user")