from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.models import Event
from core.views import send_event_reminder_to_guests

@shared_task
def send_event_reminders():
    now = timezone.now()
    today = now.date()
    one_day_from_now = today + timedelta(days=1)
    two_days_from_now = today + timedelta(days=2)
    three_days_from_now = today + timedelta(days=3)
    print(f"[Celery] Task started at {now}")
    events = Event.objects.filter(date__date__in=[today, one_day_from_now, two_days_from_now, three_days_from_now])
    print(f"[Celery] Checking for events on: {today}, {one_day_from_now}, {two_days_from_now}, {three_days_from_now}. Events found: {events.count()}")
    for event in events:
        print(f"[Celery] Event: {event.header_text} at {event.date}")
        rsvps = event.rsvps.filter(email__isnull=False).exclude(email='')
        print(f"[Celery] RSVPs with emails: {rsvps.count()}")
        for rsvp in rsvps:
            print(f"[Celery] Sending to: {rsvp.email}")
        send_event_reminder_to_guests(event)