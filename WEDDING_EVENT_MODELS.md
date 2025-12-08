# Wedding Event Models - Implementation Summary

## Overview
Created a new event type system with comprehensive wedding event models following the complete wedding documentation specifications.

## Models Created

### 1. EventType
**Purpose**: Define different types of events (Wedding, Birthday, Corporate)

**Fields**:
- `name`: Choice field (wedding, birthday, corporate)
- `display_name`: Display name for the event type
- `description`: Optional description
- `is_active`: Active status
- `created_at`, `updated_at`: Timestamps

**Usage**: 
```python
# Create event types
wedding_type = EventType.objects.create(
    name='wedding',
    display_name='Wedding',
    description='Wedding events and celebrations'
)
```

---

### 2. WeddingEvent
**Purpose**: Main wedding event model with all wedding-specific fields

**Key Sections**:

#### Basic Information
- `event_title`: "Sophia & Alexander"
- `logo_text`: "S & A"
- `event_date`: DateTime field
- `event_location`: "Lusaka, Zambia"

#### Color Theme
- `primary_color`: #f8f5f2 (hex)
- `secondary_color`: #e8d5c4 (hex)
- `accent_color`: #c8a97e (hex)

#### Couple Information
- Bride: name, image, description
- Groom: name, image, description

#### Love Story
- `story_paragraph1`: Opening story
- `story_highlight`: Special quote
- `story_paragraph2`: Continuation

#### Venue Information
- `venue_name`, `venue_description`, `venue_address`
- `ceremony_time`, `reception_time`
- `parking_info`, `transport_info`

#### Map Location (Dual Options)
- `map_method`: 'search' or 'google'
- OpenStreetMap: latitude, longitude, place_name, formatted_address
- Google Maps: google_maps_url

#### Wedding Details
- `dress_code`, `dress_code_description`
- `accommodation_name`, `accommodation_address`

#### RSVP Settings
- `rsvp_title`, `rsvp_subtitle`
- `rsvp_background_image`

#### Footer
- `footer_logo`, `footer_text`, `footer_date_location`

#### System Fields
- `slug`: Auto-generated (bride-groom-yyyy-mm-dd)
- `is_published`: Publish status
- `is_past_event`: Auto-calculated
- `invitations_sent`: Tracking field

**Properties**:
- `couple_names`: Returns "Bride & Groom"
- `event_api_url`: API endpoint URL
- `event_public_url`: Public website URL

---

### 3. WeddingSliderImage
**Purpose**: Hero slider images (repeatable)

**Fields**:
- `wedding`: ForeignKey to WeddingEvent
- `image`: CloudinaryField
- `title`: Main heading
- `subtitle`: Secondary text
- `date_text`: Date/location text
- `order`: Display order

---

### 4. WeddingBridesmaid
**Purpose**: Bridesmaids (repeatable)

**Fields**:
- `wedding`: ForeignKey to WeddingEvent
- `name`: Full name
- `role`: "Maid of Honor", "Bridesmaid"
- `description`: Relationship description
- `image`: CloudinaryField
- `order`: Display order

---

### 5. WeddingGroomsman
**Purpose**: Groomsmen (repeatable)

**Fields**:
- `wedding`: ForeignKey to WeddingEvent
- `name`: Full name
- `role`: "Best Man", "Groomsman"
- `description`: Relationship description
- `image`: CloudinaryField
- `order`: Display order

---

### 6. WeddingGalleryImage
**Purpose**: Gallery images (repeatable)

**Fields**:
- `wedding`: ForeignKey to WeddingEvent
- `image`: CloudinaryField
- `alt_text`: Accessibility description
- `is_featured`: Featured flag
- `uploaded_at`: Timestamp
- `order`: Display order

---

### 7. WeddingRSVP
**Purpose**: RSVP responses

**Fields**:
- `wedding`: ForeignKey to WeddingEvent
- `full_name`: Guest name
- `email`: Optional email
- `phone_number`: Optional phone
- `number_of_guests`: Guest count
- `attending`: 'yes', 'no', 'maybe'
- `dietary_requirements`: Special dietary needs
- `message`: Special notes
- `created_at`, `updated_at`: Timestamps

---

## Next Steps

### 1. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Initial Event Types
```python
from core.models import EventType

# Create event types
EventType.objects.create(name='wedding', display_name='Wedding', is_active=True)
EventType.objects.create(name='birthday', display_name='Birthday', is_active=True)
EventType.objects.create(name='corporate', display_name='Corporate Event', is_active=True)
```

### 3. Register Models in Admin
Update `core/admin.py` to register the new models with inline editors for repeatable sections.

### 4. Create Serializers
Create serializers in `core/serializers.py` for API endpoints.

### 5. Create Views and URLs
Set up API endpoints for:
- Wedding event CRUD
- Slider images management
- Bridesmaids/Groomsmen management
- Gallery images management
- RSVP submissions

---

## Features Implemented

✅ **Event Type System**: Wedding, Birthday, Corporate
✅ **Comprehensive Wedding Model**: All fields from documentation
✅ **Color Theme Support**: Primary, secondary, accent colors
✅ **Dual Map Options**: OpenStreetMap + Google Maps
✅ **Repeatable Sections**: Sliders, bridesmaids, groomsmen, gallery
✅ **RSVP System**: Full RSVP management
✅ **Auto Slug Generation**: bride-groom-yyyy-mm-dd format
✅ **Past Event Detection**: Automatic status updates
✅ **Cloudinary Integration**: All image uploads
✅ **Help Text**: Comprehensive field descriptions

---

## Database Structure

```
EventType (1) ──────> (Many) WeddingEvent
                           │
                           ├──> (Many) WeddingSliderImage
                           ├──> (Many) WeddingBridesmaid
                           ├──> (Many) WeddingGroomsman
                           ├──> (Many) WeddingGalleryImage
                           └──> (Many) WeddingRSVP
```

---

## Original Event Model
The original `Event` model remains **UNTOUCHED** and continues to work as before. This new system runs in parallel.

---

## API Endpoints (To Be Created)

Suggested URL structure:
```
/api/wedding-events/                    # List/Create
/api/wedding-events/<slug>/             # Retrieve/Update/Delete
/api/wedding-events/<slug>/sliders/     # Slider images
/api/wedding-events/<slug>/bridesmaids/ # Bridesmaids
/api/wedding-events/<slug>/groomsmen/   # Groomsmen
/api/wedding-events/<slug>/gallery/     # Gallery images
/api/wedding-events/<slug>/rsvp/        # RSVP submission
/api/wedding-events/<slug>/rsvps/       # RSVP list (admin)
```

---

## Notes

- All images use Cloudinary with organized folder structure (`wedding/bride/`, `wedding/slider/`, etc.)
- Slug format: `sophia-alexander-2024-10-14`
- Automatic past event detection based on `event_date`
- Order fields allow custom sorting of repeatable items
- Comprehensive help text for all fields
- Ready for Django admin integration with inline editors

---

**Status**: ✅ Models created and ready for migration
**Next**: Run migrations and set up admin interface
