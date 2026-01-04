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
Version | Date       | Change Description                                  | Reference
------------------------------------------------------------
v1.0    | 2026-01-04 | Added Event list and detail views                  | DEV-120
v1.1    | 2026-01-04 | Added holding page view for URL testing            | DEV-119
============================================================
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Event

# Temporary holding page view for new urls with no view
class HoldingPageView(TemplateView):

    template_name = "main/holding.html"


