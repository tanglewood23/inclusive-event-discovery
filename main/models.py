'''
============================================================
File Name: models.py
Brief Description:
Defines the core data model for the Inclusive Event Discovery
prototype. Includes Event and EventAccessibilityProfile,
with a system-derived sensory_level to reduce organiser bias.

Author: Gavin Plucknett
Created: 2026-01-01
Current Version: v1.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                    |Reference
------------------------------------------------------------
v1.0    | 2026-01-06 | Create intital prototype models.      | DEV-118
============================================================
'''

#Import required libraries

from django.db import models
from django.contrib.auth.models import User

# Accessibility profile model
class AccessibilityProfile(models.Model):

#Create field dropdown choices
    NOISE_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    LIGHTING_CHOICES = [
        ("NATURAL", "Natural"),
        ("STANDARD", "Standard"),
        ("BRIGHT", "Bright"),
        ("FLASHING", "Flashing"),
    ]

    CROWD_CHOICES = [
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large"),
    ]

    SENSORY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    #Create Fields 
    wheelchair_access = models.BooleanField()
    accessible_toilets = models.BooleanField(blank=True, null=True)
    quiet_space_available = models.BooleanField(blank=True, null=True)
    noise_level = models.CharField(max_length=10, choices=NOISE_CHOICES)
    lighting_conditions = models.CharField(max_length=10, choices=LIGHTING_CHOICES)
    crowd_level = models.CharField(max_length=10, choices=CROWD_CHOICES)
    sensory_level = models.CharField(max_length=10,choices=SENSORY_CHOICES)
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Define display name
    def __str__(self) -> str:
        return f"AccessibilityProfile #{self.pk}"
    
    #Define plural name for admin console
    class Meta:
        verbose_name_plural = 'AccessibilityProfiles'

# Event Model
class Event(models.Model):

    #Create field dropdown choices
    CATEGORY_CHOICES = [
        ("SPORTS", "Sports"),
        ("ARTS", "Arts"),
        ("EDUCATION", "Education"),
        ("SOCIAL", "Social"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PUBLISHED", "Published"),
        ("CANCELLED", "Cancelled"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    age_min = models.IntegerField(blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location_text = models.CharField(max_length=255)
    postcode = models.CharField(max_length=12, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    booking_required = models.BooleanField(default=False)
    booking_url = models.URLField(blank=True)
    accessibility_profile = models.OneToOneField(AccessibilityProfile,on_delete=models.CASCADE,related_name="event",)
    created_by_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_events",)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="DRAFT")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Define display name
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Events'
    