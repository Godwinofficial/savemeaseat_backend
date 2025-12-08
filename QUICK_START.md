# 🚀 Wedding Event API - Quick Start

## 1️⃣ Initialize Event Types (One-time)
```bash
python manage.py shell < initialize_event_types.py
```

## 2️⃣ Start Server
```bash
python manage.py runserver
```

## 3️⃣ Create Your First Wedding

### Using cURL:
```bash
curl -X POST http://localhost:8000/api/wedding-events/ \
  -F "event_type_id=1" \
  -F "event_title=Sophia & Alexander" \
  -F "event_date=2024-10-14T16:00:00" \
  -F "event_location=Lusaka, Zambia" \
  -F "bride_name=Sophia" \
  -F "bride_image=@path/to/bride.jpg" \
  -F "groom_name=Alexander" \
  -F "groom_image=@path/to/groom.jpg" \
  -F "venue_name=The Glass House" \
  -F "venue_address=123 Modern Avenue, Lusaka" \
  -F "ceremony_time=16:00:00" \
  -F "primary_color=#f8f5f2" \
  -F "is_published=true"
```

### Using Python:
```python
import requests

url = "http://localhost:8000/api/wedding-events/"

# Get event type ID first
event_types = requests.get("http://localhost:8000/api/event-types/").json()
wedding_type_id = event_types[0]['id']

# Prepare data
data = {
    'event_type_id': wedding_type_id,
    'event_title': 'Sophia & Alexander',
    'event_date': '2024-10-14T16:00:00',
    'event_location': 'Lusaka, Zambia',
    'bride_name': 'Sophia',
    'groom_name': 'Alexander',
    'venue_name': 'The Glass House',
    'venue_address': '123 Modern Avenue, Lusaka',
    'ceremony_time': '16:00:00',
    'primary_color': '#f8f5f2',
    'is_published': True
}

files = {
    'bride_image': open('bride.jpg', 'rb'),
    'groom_image': open('groom.jpg', 'rb')
}

response = requests.post(url, data=data, files=files)
print(response.json())
```

### Using JavaScript (Fetch):
```javascript
const formData = new FormData();
formData.append('event_type_id', '1');
formData.append('event_title', 'Sophia & Alexander');
formData.append('event_date', '2024-10-14T16:00:00');
formData.append('event_location', 'Lusaka, Zambia');
formData.append('bride_name', 'Sophia');
formData.append('bride_image', brideImageFile);
formData.append('groom_name', 'Alexander');
formData.append('groom_image', groomImageFile);
formData.append('venue_name', 'The Glass House');
formData.append('venue_address', '123 Modern Avenue, Lusaka');
formData.append('ceremony_time', '16:00:00');
formData.append('primary_color', '#f8f5f2');
formData.append('is_published', 'true');

fetch('http://localhost:8000/api/wedding-events/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 4️⃣ Add Slider Images
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/sliders/ \
  -F "image=@slide1.jpg" \
  -F "title=Sophia & Alexander" \
  -F "subtitle=We are getting married" \
  -F "date_text=October 14, 2024 • Lusaka" \
  -F "order=0"
```

## 5️⃣ Add Bridesmaids
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/bridesmaids/ \
  -F "name=Emma Wilson" \
  -F "role=Maid of Honor" \
  -F "description=Sister and best friend" \
  -F "image=@bridesmaid1.jpg" \
  -F "order=0"
```

## 6️⃣ Add Groomsmen
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/groomsmen/ \
  -F "name=James Thompson" \
  -F "role=Best Man" \
  -F "description=Childhood friend" \
  -F "image=@groomsman1.jpg" \
  -F "order=0"
```

## 7️⃣ Add Gallery Images
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/gallery/ \
  -F "image=@gallery1.jpg" \
  -F "alt_text=Couple photo 1" \
  -F "is_featured=false" \
  -F "order=0"
```

## 8️⃣ Submit RSVP
```bash
curl -X POST http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/rsvp/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+260971234567",
    "number_of_guests": 2,
    "attending": "yes",
    "dietary_requirements": "Vegetarian",
    "message": "Looking forward to celebrating with you!"
  }'
```

## 9️⃣ Get Wedding Details
```bash
curl http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/
```

## 🔟 Export RSVPs
```bash
curl http://localhost:8000/api/wedding-events/sophia-alexander-2024-10-14/rsvp/export/ -o rsvps.csv
```

---

## 📋 Essential Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| List event types | GET | `/api/event-types/` |
| Create wedding | POST | `/api/wedding-events/` |
| Get wedding | GET | `/api/wedding-events/{slug}/` |
| Update wedding | PUT/PATCH | `/api/wedding-events/{slug}/` |
| Delete wedding | DELETE | `/api/wedding-events/{slug}/` |
| Add slider | POST | `/api/wedding-events/{slug}/sliders/` |
| Add bridesmaid | POST | `/api/wedding-events/{slug}/bridesmaids/` |
| Add groomsman | POST | `/api/wedding-events/{slug}/groomsmen/` |
| Add gallery image | POST | `/api/wedding-events/{slug}/gallery/` |
| Submit RSVP | POST | `/api/wedding-events/{slug}/rsvp/` |
| List RSVPs | GET | `/api/wedding-events/{slug}/rsvps/` |
| Export RSVPs | GET | `/api/wedding-events/{slug}/rsvp/export/` |

---

## 🎯 Required Fields for Wedding Creation

**Minimum Required:**
- `event_type_id`: 1 (wedding)
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

**Everything else is optional!**

---

## 🎨 Color Theme Defaults

If not provided, these colors are used:
- `primary_color`: #f8f5f2
- `secondary_color`: #e8d5c4
- `accent_color`: #c8a97e

---

## 🗺️ Map Options

**Option 1: OpenStreetMap (Interactive Search)**
```json
{
  "map_method": "search",
  "map_latitude": "-15.4167",
  "map_longitude": "28.2833",
  "map_place_name": "Lusaka City Center",
  "map_formatted_address": "Lusaka, Zambia"
}
```

**Option 2: Google Maps Embed**
```json
{
  "map_method": "google",
  "google_maps_url": "https://www.google.com/maps?q=-12.808,28.214&z=15&output=embed"
}
```

---

## 📱 RSVP Attending Options

- `"yes"`: Yes, I will attend
- `"no"`: No, I cannot attend
- `"maybe"`: Maybe

---

## 🔗 Useful Links

- **Full API Documentation**: `WEDDING_API_DOCUMENTATION.md`
- **Model Documentation**: `WEDDING_EVENT_MODELS.md`
- **Setup Guide**: `SETUP_COMPLETE.md`

---

## ✅ Checklist

- [ ] Run `initialize_event_types.py`
- [ ] Start server
- [ ] Create first wedding event
- [ ] Add slider images
- [ ] Add bridesmaids
- [ ] Add groomsmen
- [ ] Add gallery images
- [ ] Test RSVP submission
- [ ] Export RSVPs to CSV

---

**Ready to go! 🎉**
