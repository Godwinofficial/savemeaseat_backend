# Wedding Event API Documentation

## Base URL
```
http://localhost:8000/api/
https://savemeaseat-backend.onrender.com/api/
```

---

## Authentication
Currently, all endpoints are open. Add authentication as needed for production.

---

## API Endpoints

### 1. Event Types

#### List Event Types
```http
GET /api/event-types/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "wedding",
    "display_name": "Wedding",
    "description": "Wedding events and celebrations",
    "is_active": true,
    "created_at": "2025-10-31T20:00:00Z"
  }
]
```

---

### 2. Wedding Events

#### Create Wedding Event
```http
POST /api/wedding-events/
Content-Type: multipart/form-data
```

**Required Fields:**
- `event_type_id`: ID of wedding event type
- `event_title`: "Sophia & Alexander"
- `event_date`: "2024-10-14T16:00:00"
- `event_location`: "Lusaka, Zambia"
- `bride_name`: "Sophia"
- `bride_image`: File upload
- `groom_name`: "Alexander"
- `groom_image`: File upload
- `venue_name`: "The Glass House"
- `venue_address`: "123 Modern Avenue, Lusaka"
- `ceremony_time`: "16:00:00"

**Optional Fields:**
- `logo_text`: "S & A"
- `primary_color`: "#f8f5f2"
- `secondary_color`: "#e8d5c4"
- `accent_color`: "#c8a97e"
- `countdown_title`: "Counting Down to Our Special Day"
- `bride_description`: "Art Director & lover of beautiful things"
- `groom_description`: "Architect & seeker of beauty"
- `story_paragraph1`: "We met five years ago..."
- `story_highlight`: "The best love is..."
- `story_paragraph2`: "After three years..."
- `venue_description`: "Modern architectural marvel..."
- `reception_time`: "18:00:00"
- `parking_info`: "Valet parking available"
- `transport_info`: "5-minute walk from station"
- `map_method`: "search" or "google"
- `map_latitude`: "-15.4167"
- `map_longitude`: "28.2833"
- `map_place_name`: "Lusaka City Center"
- `map_formatted_address`: "Lusaka, Zambia"
- `google_maps_url`: "https://www.google.com/maps?q=-12.808,28.214&z=15&output=embed"
- `dress_code`: "Formal Attire"
- `dress_code_description`: "Black Tie Optional"
- `accommodation_name`: "The Modernist Hotel"
- `accommodation_address`: "456 Design Street, Lusaka"
- `rsvp_title`: "RSVP"
- `rsvp_subtitle`: "Kindly respond by September 1st"
- `rsvp_background_image`: File upload
- `footer_logo`: "Sophia & Alexander"
- `footer_text`: "We are so excited to celebrate"
- `footer_date_location`: "October 14, 2024 • Lusaka"
- `is_published`: true/false

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/api/wedding-events/ \
  -F "event_type_id=1" \
  -F "event_title=Sophia & Alexander" \
  -F "event_date=2024-10-14T16:00:00" \
  -F "event_location=Lusaka, Zambia" \
  -F "bride_name=Sophia" \
  -F "bride_image=@bride.jpg" \
  -F "groom_name=Alexander" \
  -F "groom_image=@groom.jpg" \
  -F "venue_name=The Glass House" \
  -F "venue_address=123 Modern Avenue, Lusaka" \
  -F "ceremony_time=16:00:00"
```

**Response:**
```json
{
  "id": 1,
  "slug": "sophia-alexander-2024-10-14",
  "event_title": "Sophia & Alexander",
  "couple_names": "Sophia & Groom",
  "event_api_url": "https://savemeaseat-backend.onrender.com/api/wedding/sophia-alexander-2024-10-14/",
  "event_public_url": "https://savemeaseat-frontend.vercel.app/wedding/sophia-alexander-2024-10-14/",
  ...
}
```

#### List All Wedding Events
```http
GET /api/wedding-events/
```

#### Get Wedding Event Details
```http
GET /api/wedding-events/{slug}/
```

**Example:**
```http
GET /api/wedding-events/sophia-alexander-2024-10-14/
```

**Response includes:**
- All wedding details
- Nested slider_images array
- Nested bridesmaids array
- Nested groomsmen array
- Nested gallery_images array
- Nested rsvps array

#### Update Wedding Event
```http
PUT /api/wedding-events/{slug}/
PATCH /api/wedding-events/{slug}/
Content-Type: multipart/form-data
```

#### Delete Wedding Event
```http
DELETE /api/wedding-events/{slug}/
```

---

### 3. Wedding Slider Images

#### Add Slider Image
```http
POST /api/wedding-events/{slug}/sliders/
Content-Type: multipart/form-data
```

**Fields:**
- `image`: File upload (required)
- `title`: "Sophia & Alexander" (required)
- `subtitle`: "We are getting married"
- `date_text`: "October 14, 2024 • Lusaka"
- `order`: 0 (for sorting)

**Example:**
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/sliders/ \
  -F "image=@slide1.jpg" \
  -F "title=Sophia & Alexander" \
  -F "subtitle=We are getting married" \
  -F "date_text=October 14, 2024 • Lusaka" \
  -F "order=0"
```

#### List Slider Images
```http
GET /api/wedding-events/{slug}/sliders/
```

#### Update Slider Image
```http
PUT /api/wedding-sliders/{id}/
PATCH /api/wedding-sliders/{id}/
```

#### Delete Slider Image
```http
DELETE /api/wedding-sliders/{id}/
```

---

### 4. Wedding Bridesmaids

#### Add Bridesmaid
```http
POST /api/wedding-events/{slug}/bridesmaids/
Content-Type: multipart/form-data
```

**Fields:**
- `name`: "Emma Wilson" (required)
- `role`: "Maid of Honor" (required)
- `description`: "Sister and best friend"
- `image`: File upload (required)
- `order`: 0

**Example:**
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/bridesmaids/ \
  -F "name=Emma Wilson" \
  -F "role=Maid of Honor" \
  -F "description=Sister and best friend" \
  -F "image=@bridesmaid1.jpg" \
  -F "order=0"
```

#### List Bridesmaids
```http
GET /api/wedding-events/{slug}/bridesmaids/
```

#### Update Bridesmaid
```http
PUT /api/wedding-bridesmaids/{id}/
PATCH /api/wedding-bridesmaids/{id}/
```

#### Delete Bridesmaid
```http
DELETE /api/wedding-bridesmaids/{id}/
```

---

### 5. Wedding Groomsmen

#### Add Groomsman
```http
POST /api/wedding-events/{slug}/groomsmen/
Content-Type: multipart/form-data
```

**Fields:**
- `name`: "James Thompson" (required)
- `role`: "Best Man" (required)
- `description`: "Childhood friend"
- `image`: File upload (required)
- `order`: 0

**Example:**
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/groomsmen/ \
  -F "name=James Thompson" \
  -F "role=Best Man" \
  -F "description=Childhood friend" \
  -F "image=@groomsman1.jpg" \
  -F "order=0"
```

#### List Groomsmen
```http
GET /api/wedding-events/{slug}/groomsmen/
```

#### Update Groomsman
```http
PUT /api/wedding-groomsmen/{id}/
PATCH /api/wedding-groomsmen/{id}/
```

#### Delete Groomsman
```http
DELETE /api/wedding-groomsmen/{id}/
```

---

### 6. Wedding Gallery

#### Add Gallery Image
```http
POST /api/wedding-events/{slug}/gallery/
Content-Type: multipart/form-data
```

**Fields:**
- `image`: File upload (required)
- `alt_text`: "Couple photo 1"
- `is_featured`: true/false
- `order`: 0

**Example:**
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/gallery/ \
  -F "image=@gallery1.jpg" \
  -F "alt_text=Couple photo 1" \
  -F "is_featured=false" \
  -F "order=0"
```

#### List Gallery Images
```http
GET /api/wedding-events/{slug}/gallery/
```

#### Update Gallery Image
```http
PUT /api/wedding-gallery/{id}/
PATCH /api/wedding-gallery/{id}/
```

#### Delete Gallery Image
```http
DELETE /api/wedding-gallery/{id}/
```

---

### 7. Wedding RSVP

#### Submit RSVP
```http
POST /api/wedding-events/{slug}/rsvp/
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+260971234567",
  "number_of_guests": 2,
  "attending": "yes",
  "dietary_requirements": "Vegetarian",
  "message": "Looking forward to celebrating with you!"
}
```

**Attending Options:**
- `"yes"`: Yes, I will attend
- `"no"`: No, I cannot attend
- `"maybe"`: Maybe

**Response:**
```json
{
  "success": true,
  "id": 1,
  "message": "RSVP submitted successfully"
}
```

#### List RSVPs (Admin)
```http
GET /api/wedding-events/{slug}/rsvps/
```

#### Export RSVPs to CSV
```http
GET /api/wedding-events/{slug}/rsvp/export/
```

Downloads a CSV file with all RSVP data.

---

## Complete Workflow Example

### 1. Create Event Type (One-time setup)
```bash
# Create wedding event type in Django admin or shell
python manage.py shell
>>> from core.models import EventType
>>> EventType.objects.create(name='wedding', display_name='Wedding', is_active=True)
```

### 2. Create Wedding Event
```bash
curl -X POST http://localhost:8000/api/wedding-events/ \
  -F "event_type_id=1" \
  -F "event_title=Sophia & Alexander" \
  -F "event_date=2024-10-14T16:00:00" \
  -F "event_location=Lusaka, Zambia" \
  -F "bride_name=Sophia" \
  -F "bride_image=@bride.jpg" \
  -F "groom_name=Alexander" \
  -F "groom_image=@groom.jpg" \
  -F "venue_name=The Glass House" \
  -F "venue_address=123 Modern Avenue, Lusaka" \
  -F "ceremony_time=16:00:00" \
  -F "primary_color=#f8f5f2" \
  -F "is_published=true"
```

### 3. Add Slider Images
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/sliders/ \
  -F "image=@slide1.jpg" \
  -F "title=Sophia & Alexander" \
  -F "subtitle=We are getting married" \
  -F "order=0"
```

### 4. Add Bridesmaids
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/bridesmaids/ \
  -F "name=Emma Wilson" \
  -F "role=Maid of Honor" \
  -F "image=@bridesmaid1.jpg" \
  -F "order=0"
```

### 5. Add Groomsmen
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/groomsmen/ \
  -F "name=James Thompson" \
  -F "role=Best Man" \
  -F "image=@groomsman1.jpg" \
  -F "order=0"
```

### 6. Add Gallery Images
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/gallery/ \
  -F "image=@gallery1.jpg" \
  -F "alt_text=Couple photo 1" \
  -F "order=0"
```

### 7. Get Complete Wedding Data
```bash
curl http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data provided",
  "details": {
    "event_title": ["This field is required."]
  }
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 405 Method Not Allowed
```json
{
  "error": "Invalid method"
}
```

---

## Image Upload Notes

1. **Supported Formats**: JPG, JPEG, PNG, GIF, WEBP
2. **Storage**: All images are uploaded to Cloudinary
3. **Folder Structure**:
   - Bride images: `wedding/bride/`
   - Groom images: `wedding/groom/`
   - Slider images: `wedding/slider/`
   - Bridesmaid images: `wedding/bridesmaids/`
   - Groomsman images: `wedding/groomsmen/`
   - Gallery images: `wedding/gallery/`
   - RSVP background: `wedding/rsvp/`

---

## Testing with Postman

1. **Create Wedding Event**:
   - Method: POST
   - URL: `http://localhost:8000/api/wedding-events/`
   - Body: form-data
   - Add all required fields and file uploads

2. **Get Wedding Event**:
   - Method: GET
   - URL: `http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/`

3. **Submit RSVP**:
   - Method: POST
   - URL: `http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/rsvp/`
   - Body: raw JSON

---

## Next Steps

1. ✅ Models created
2. ✅ Serializers created
3. ✅ Views created
4. ✅ URLs configured
5. ⏳ Create Django admin interface
6. ⏳ Add authentication
7. ⏳ Add permissions
8. ⏳ Add pagination
9. ⏳ Add filtering and search
10. ⏳ Add API documentation (Swagger/ReDoc)

---

**Status**: ✅ All API endpoints are ready and functional!
