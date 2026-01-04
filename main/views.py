"""
============================================================
File Name: views.py
Brief Description:
View logic for the prototype. Includes temporary holding views
used during early development and URL testing.

Author: Gavin Plucknett
Created: 2026-01-04
Current Version: v1.1

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                      | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Added holding page view for URL testing | DEV-119          
v1.1    | 2026-01-04 | Added events and event detail views.    | DEV-120          
============================================================
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Event

# Temporary holding page view for new urls with no view
class HoldingPageView(TemplateView):

    template_name = "main/holding.html"

# Event list view
class EventListView(ListView):
    
    # Displays a list of published events for browsing/discovery.
    model = Event
    template_name = "main/event_list.html"
    context_object_name = "events"
    paginate_by = None 

    # Get Published Events Query
    def get_queryset(self):
        # Prototype scope: show published events first; if you don't use status yet,
        # change this to: return Event.objects.all().order_by("-start_datetime")
        return Event.objects.filter(status="PUBLISHED").order_by("start_datetime")


class EventDetailView(DetailView):

    #Displays a single event including event detail and accessibility information.

    model = Event
    template_name = "main/event_detail.html"
    context_object_name = "event"
