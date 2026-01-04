"""
============================================================
File Name: urls.py
Brief Description:
URL routing for the prototype. Defines routes for browsing
events and viewing event detail pages.

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                   | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Added event list and detail routes   | DEV-119
============================================================
"""

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("events/", views.HoldingPageView.as_view(), name="event_list"),
    path("events/<int:pk>/", views.HoldingPageView.as_view(), name="event_detail"),
]