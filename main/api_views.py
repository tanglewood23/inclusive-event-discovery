"""
============================================================
File Name: api_views.py
Brief Description:
Read-only REST API views for the prototype. Provides endpoints
to list events and retrieve event details including linked
accessibility information.

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                     | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Initial read-only API views            | DEV-123
============================================================
"""

from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

# Read only endpoint return published Event List
class EventListAPIView(generics.ListAPIView):

    # Set serializer
    serializer_class = EventSerializer

    # return query events
    def get_queryset(self):
        return Event.objects.filter(status="PUBLISHED").order_by("start_datetime")

# Read only endpoint return event details
class EventDetailAPIView(generics.RetrieveAPIView):
    
    #Set serializer
    serializer_class = EventSerializer

    # Return Event details
    queryset = Event.objects.all()
