# Inclusive Event Discovery Platform

**Author:** Gavin Plucknett
**Module:** Databases and Advanced Data Techniques (Project Template 2.1)
**Repository:** Inclusive Event Discovery (Phase 2 Prototype)

---

## 1. Project Overview

This project is a **prototype inclusive event discovery platform** designed to support **neurodivergent individuals, disabled people, and families with SEND needs** when deciding whether to attend events.

The core aim is to reduce uncertainty by providing **structured, sensory-aware accessibility information** alongside standard event details. Accessibility is treated as **first-class data**, not an optional free-text add-on.

The system focuses on:

* Clear event discovery
* Structured sensory and accessibility attributes
* Low cognitive load presentation
* Extensible, normalised data modelling

This repository represents **Iteration / Phase 2** of the prototype.

---

## 2. Scope of the Prototype (Phase 2)

The prototype is intentionally scoped to demonstrate **data modelling quality, integrity, and traceability**, rather than full production features.

### Included in Phase 2

* Event discovery (read-only user view)
* Structured event-level accessibility modelling
* Normalised lookup/reference data
* Admin-managed reference data
* REST-style JSON API for events

### Explicitly Excluded (by design)

* Ticketing and payments
* User accounts for attendees
* Automated decision-making or scoring
* Venue-level accessibility profiles (planned future work)
* Media uploads (planned future work)

These exclusions are deliberate and justified in the design documentation.

---

## 3. Core Data Model

The Phase 2 data model consists of the following **core entities**:

### Event

Represents a single event that users may consider attending.

* Title, description, date/time, location
* Category (normalised lookup)
* Linked accessibility profile
* Optional venue reference

### AccessibilityProfile

Stores **event-specific accessibility characteristics**, including:

* Wheelchair access
* Accessible toilets (tri-state: yes / no / unknown)
* Quiet space availability (tri-state)
* Sensory-related attributes (noise, lighting, crowd, overall sensory load)

### LookupOption

A normalised reference entity used for **coded choices**, such as:

* Event categories (e.g. Social, Sports)
* Sensory and accessibility levels (e.g. Low / Medium / High)

Lookup options are reusable, administrable, and decoupled from application logic.

### SensoryCategory

Defines **semantic groupings** for sensory-related lookup options, such as:

* Noise
* Lighting
* Crowd
* Overall Sensory Load

Sensory relevance is derived **relationally**, not hard-coded.

### Venue (Basic)

A minimal venue entity included to support future extension. Venue-level accessibility is intentionally deferred.

---

## 4. Sensory Modelling Approach (Key Design Decision)

A key design decision in Phase 2 is that **sensory meaning is not hard-coded**.

Instead:

* `SensoryCategory` defines *what counts as a sensory dimension*
* `LookupOption` references a `SensoryCategory` where applicable
* Event categories do **not** have a sensory category

This approach:

* Avoids brittle enum-based logic
* Allows new sensory dimensions to be added without code changes
* Improves extensibility and maintainability

Validation rules ensure:

* Event categories cannot be assigned a sensory category
* Sensory-related lookup options must be assigned a sensory category

---

## 5. Admin Interface

The Django admin interface is used intentionally as a **controlled authoring environment**.

Admin users can:

* Manage sensory categories
* Create and maintain lookup options
* Assign sensory categories at lookup option creation
* Create events and accessibility profiles

Admin forms include:

* Filtering and ordering for reference data
* Autocomplete fields for FK-heavy models
* Validation to prevent invalid sensory assignments

This demonstrates practical governance of structured accessibility data.

---

## 6. Seed Data

Reference data is seeded using **Django fixtures**, including:

### Sensory Categories

* Noise
* Lighting
* Crowd
* Overall Sensory Load

### Lookup Options

* Event categories (e.g. Social, Sports)
* Sensory levels (Low / Medium / High) grouped under the relevant sensory category

Fixtures are located in:

```
main/fixtures/
```

They can be loaded using:

```bash
python manage.py loaddata sensory_categories.json
python manage.py loaddata lookup_options.json
```

---

## 7. API Output

The prototype exposes a read-only JSON API for published events.

Accessibility data is returned in a **structured and human-readable format**, for example:

```json
"noise_level": {
  "code": "MEDIUM",
  "label": "Medium"
}
```

This preserves machine-readability while supporting user-facing clarity.

---

## 8. Technology Stack

* **Backend:** Django (Python)
* **Database:** SQLite (prototype)
* **ORM:** Django ORM
* **API:** Django REST Framework
* **Admin:** Django Admin

The stack was chosen to prioritise data integrity, rapid iteration, and auditability.

---

## 9. Academic Alignment

This project aligns with **Project Template 2.1** by demonstrating:

* Strong relational data modelling
* Normalisation and referential integrity
* Full CRUD (admin-controlled)
* Clear traceability from requirements to implementation
* Ethical and inclusive design decisions

Design choices are grounded in participatory research and inclusive design principles, as documented in the accompanying report.

---

## 10. How to Run the Project

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sensory_categories.json
python manage.py loaddata lookup_options.json
python manage.py runserver
```

Access:

* Admin: `http://127.0.0.1:8000/admin/`
* Events API: `http://127.0.0.1:8000/api/events/`

---

## 11. Notes for the Marker

* The prototype intentionally prioritises **clarity and correctness of data modelling** over feature breadth.
* Accessibility attributes are descriptive, not prescriptive; the system supports informed decision-making rather than automated suitability judgments.
* Several entities (venue accessibility, media, reviews) are intentionally deferred and documented as future work.

This repository should be read alongside the submitted design report for full context.
