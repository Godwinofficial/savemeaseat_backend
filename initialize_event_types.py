"""
Initialize Event Types
Run this script to create the initial event types in the database.

Usage:
    python manage.py shell < initialize_event_types.py
    
Or in Django shell:
    python manage.py shell
    >>> exec(open('initialize_event_types.py').read())
"""

from core.models import EventType

# Create event types
event_types = [
    {
        'name': 'wedding',
        'display_name': 'Wedding',
        'description': 'Wedding events and celebrations',
        'is_active': True
    },
    {
        'name': 'birthday',
        'display_name': 'Birthday',
        'description': 'Birthday parties and celebrations',
        'is_active': True
    },
    {
        'name': 'corporate',
        'display_name': 'Corporate Event',
        'description': 'Corporate events, conferences, and business gatherings',
        'is_active': True
    },
]

print("🎉 Initializing Event Types...")
print("-" * 50)

for event_type_data in event_types:
    event_type, created = EventType.objects.get_or_create(
        name=event_type_data['name'],
        defaults={
            'display_name': event_type_data['display_name'],
            'description': event_type_data['description'],
            'is_active': event_type_data['is_active']
        }
    )
    
    if created:
        print(f"✅ Created: {event_type.display_name}")
    else:
        print(f"ℹ️  Already exists: {event_type.display_name}")

print("-" * 50)
print("✨ Event types initialization complete!")
print(f"\nTotal event types: {EventType.objects.count()}")
print("\nAvailable event types:")
for et in EventType.objects.all():
    print(f"  - {et.display_name} ({et.name})")
