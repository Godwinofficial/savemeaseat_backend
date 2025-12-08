from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.models import Event, WeddingEvent  # Add other event types as needed
from core.views import send_event_reminder_to_guests, send_wedding_reminder_to_guests

@shared_task
def send_event_reminders():
    now = timezone.now()
    today = now.date()
    one_day_from_now = today + timedelta(days=1)
    two_days_from_now = today + timedelta(days=2)
    three_days_from_now = today + timedelta(days=3)
    
    # Base Events
    print(f"[Celery] Checking base events...")
    events = Event.objects.filter(date__date__in=[
        today, one_day_from_now, two_days_from_now, three_days_from_now
    ])
    for event in events:
        print(f"[Celery] Processing event: {event.header_text} on {event.date}")
        send_event_reminder_to_guests(event)
    
    # Wedding Events
    print(f"[Celery] Checking wedding events...")
    wedding_events = WeddingEvent.objects.filter(event_date__date__in=[
        today, one_day_from_now, two_days_from_now, three_days_from_now
    ])
    for event in wedding_events:
        print(f"[Celery] Processing wedding: {event.event_title} on {event.event_date}")
        send_wedding_reminder_to_guests(event)
    
    # Add other event types (Birthday, Corporate) here when their models are created
    print("[Celery] Reminder task completed")