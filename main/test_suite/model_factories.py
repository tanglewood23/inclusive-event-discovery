"""
============================================================
File Name: factories.py
Brief Description:
Factory Boy factories using Faker to generate realistic,
non-hardcoded test data for core prototype models.

Author: Gavin Plucknett
Created: 2026-01-01
Current Version: v1.1

Change Log:
------------------------------------------------------------
Version | Date       | Change Description                   | Reference
------------------------------------------------------------
v1.0    | 2026-01-01 | Initial factories                    | DEV-125
============================================================
"""

import factory
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone

from main.models import Event, AccessibilityProfile

# Set faker country
fake = Faker("en_GB")

#Create fake user
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")

#Create an AccessibilityProfile for an Event
class AccessibilityProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessibilityProfile

    # Random boolean values
    wheelchair_access = factory.Faker("boolean")
    accessible_toilets = factory.Faker("boolean")
    quiet_space_available = factory.Faker("boolean")

    # These default to LOW impact, but can be overridden in tests
    noise_level = "LOW"
    lighting_conditions = "NATURAL"
    crowd_level = "SMALL"
    
    #Create 2 sentences of notes
    additional_notes = factory.Faker("paragraph", nb_sentences=2)

# Create Events
class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    #Create Test Title and description
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=4)

    #Choose random category
    category = factory.Iterator(
        ["SPORTS", "ARTS", "EDUCATION", "SOCIAL"]
    )

    # Random min age 0-12 and max age min_age + 0-6
    age_min = factory.LazyFunction(lambda: fake.random_int(min=0, max=12))
    age_max = factory.LazyAttribute(lambda o: o.age_min + fake.random_int(min=0, max=6))

    # Event with startdate today then end date 1-4 days time
    start_datetime = factory.LazyFunction(timezone.now)
    end_datetime = factory.LazyAttribute(
        lambda o: o.start_datetime + timezone.timedelta(hours=fake.random_int(1, 4))
    )

    #Random city and postcode
    location_text = factory.Faker("city")
    postcode = factory.Faker("postcode")

    #Random price
    price = factory.LazyFunction(
        lambda: fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    )

    #Random booking details
    booking_required = factory.Faker("boolean")
    booking_url = factory.LazyAttribute(
        lambda o: fake.url() if o.booking_required else ""
    )

    #Link user an accessibility profile
    accessibility_profile = factory.SubFactory(AccessibilityProfileFactory)
    created_by_user = factory.SubFactory(UserFactory)

    status = factory.Iterator(["DRAFT", "PUBLISHED"])
