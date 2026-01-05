"""
============================================================
File Name: api_urls.py
Brief Description:
URL routing for the prototype REST API.

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                    | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Added /api/events endpoints           | DEV-123
============================================================
"""

from django.urls import path
from .api_views import EventListAPIView, EventDetailAPIView

app_name = "main_api"

urlpatterns = [
    path("events/", EventListAPIView.as_view(), name="events_list"),
    path("events/<int:pk>/", EventDetailAPIView.as_view(), name="events_detail"),
]
