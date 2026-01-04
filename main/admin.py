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

admin.site.register(Event)
admin.site.register(AccessibilityProfile)