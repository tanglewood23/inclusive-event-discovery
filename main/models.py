"""
============================================================
File Name: models.py
Brief Description:
Iteration 2 data model for Inclusive Event Discovery prototype.
Introduces LookupOption normalisation for coded value, and adds SensoryCategory to administer grouping
of accessibility-related options. Event status remains a coded
system field.

Author: Gavin Plucknett
Created: 2026-01-05
Current Version: v2.0

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                                  | Reference
------------------------------------------------------------
v2.0    | 2026-01-05 | Normalised coded choices + added Venue + categories| DEV-ITER2
============================================================
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SensoryCategory(models.Model):
    """
    Administered grouping used to organise accessibility-related options.
    Examples: Sensory, Environment, Planning.
    """
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.label

class LookupOption(models.Model):
    class OptionType(models.TextChoices):
        EVENT_CATEGORY = "EVENT_CATEGORY"
        ACCESSIBILITY_LEVEL = "ACCESSIBILITY_LEVEL"
        # (you can keep this generic if you want)

    option_type = models.CharField(
        max_length=50,
        choices=OptionType.choices,
    )

    code = models.CharField(max_length=50)     # e.g. LOW / MEDIUM / HIGH
    label = models.CharField(max_length=100)   # e.g. "Low"
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        "SensoryCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lookup_options",
        help_text="Assign for sensory-related options. Leave blank for non-sensory options."
    )

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def clean(self):
        super().clean()

        # Event categories must NOT be sensory
        if self.option_type == "EVENT_CATEGORY" and self.sensory_category_id:
            raise ValidationError({
                "sensory_category": "Event categories must not be assigned to a sensory category."
            })

        # Accessibility options SHOULD be sensory
        if self.option_type == "ACCESSIBILITY_LEVEL" and not self.sensory_category_id:
            raise ValidationError({
                "sensory_category": "Accessibility options must be assigned to a sensory category."
            })

    class Meta:
        unique_together = ("option_type", "code")
        ordering = ("option_type","display_order", "label")

    def __str__(self):
        return self.label
    
class AccessibilityProfile(models.Model):

    wheelchair_access = models.BooleanField(default=False)

    # tri-state booleans
    accessible_toilets = models.BooleanField(null=True, blank=True)
    quiet_space_available = models.BooleanField(null=True, blank=True)

    noise_level = models.ForeignKey(
        LookupOption,
        on_delete=models.PROTECT,
        related_name="noise_profiles",
        limit_choices_to={"option_type": "NOISE_LEVEL"},
    )
    lighting_conditions = models.ForeignKey(
        LookupOption,
        on_delete=models.PROTECT,
        related_name="lighting_profiles",
        limit_choices_to={"option_type": "LIGHTING_CONDITION"},
    )
    crowd_level = models.ForeignKey(
        LookupOption,
        on_delete=models.PROTECT,
        related_name="crowd_profiles",
        limit_choices_to={"option_type": "CROWD_LEVEL"},
    )
    sensory_level = models.ForeignKey(
        LookupOption,
        on_delete=models.PROTECT,
        related_name="sensory_profiles",
        limit_choices_to={"option_type": "SENSORY_LEVEL"},
    )

    additional_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"AccessibilityProfile #{self.pk}"


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT"
        PUBLISHED = "PUBLISHED"
        CANCELLED = "CANCELLED"

    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.ForeignKey(
        LookupOption,
        on_delete=models.PROTECT,
        related_name="events",
        limit_choices_to={"option_type": "EVENT_CATEGORY"},
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location_text = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20, blank=True)
    age_min = models.IntegerField(null=True, blank=True)
    age_max = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    booking_required = models.BooleanField(default=False)
    booking_url = models.URLField(blank=True)
    accessibility_profile = models.OneToOneField(AccessibilityProfile,on_delete=models.CASCADE,related_name="event",)
    created_by_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_events",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    