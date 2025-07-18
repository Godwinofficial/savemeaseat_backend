from core.views import send_event_reminder_to_guests
from core.models import Event
from django.utils import timezone

def send_reminders_job():
    now = timezone.now()
    today = now.date()
    one_day_from_now = today + timezone.timedelta(days=1)
    two_days_from_now = today + timezone.timedelta(days=2)
    three_days_from_now = today + timezone.timedelta(days=3)
    events = Event.objects.filter(date__date__in=[today, one_day_from_now, two_days_from_now, three_days_from_now])
    print(f"[APScheduler] Now: {now}, Checking for events on: {today}, {one_day_from_now}, {two_days_from_now}, {three_days_from_now}. Events found: {events.count()}")
    for event in events:
        print(f"[APScheduler] Event: {event.header_text} at {event.date}")
        send_event_reminder_to_guests(event) 