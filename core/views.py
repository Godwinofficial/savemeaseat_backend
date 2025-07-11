from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Event, RSVP, Bridesmaid, Groomsman
from .serializers import EventSerializer, BridesmaidSerializer, GroomsmanSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# Create your views here.

# NOTE: You must create core/templates/event_detail.html for the event detail page meta tags to work.

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

@csrf_exempt
def submit_rsvp(request, event_slug):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = get_object_or_404(Event, slug=event_slug)
        rsvp = RSVP.objects.create(
            event=event,
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            number_of_guests=data.get('number_of_guests', 1),
            attending=data.get('attending')
        )
        
        # Automatically send reminder if event is within 2 days or today
        try:
            today = timezone.now().date()
            event_date = event.date
            if event_date:
                days_until_event = (event_date - today).days
                
                if days_until_event <= 2 and days_until_event >= 0:
                    send_event_reminder(event)
        except Exception as e:
            # Log error but don't break RSVP submission
            print(f"Error sending automatic reminder: {e}")
        
        return JsonResponse({'success': True, 'id': rsvp.id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def export_rsvp_csv(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    rsvps = event.rsvps.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="rsvp_{event_slug}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Phone Number', 'Number of Guests', 'Attending', 'Created At'])
    for rsvp in rsvps:
        writer.writerow([rsvp.full_name, rsvp.email, rsvp.phone_number, rsvp.number_of_guests, rsvp.attending, rsvp.created_at])
    return response

class BridesmaidListCreateView(generics.ListCreateAPIView):
    queryset = Bridesmaid.objects.all()
    serializer_class = BridesmaidSerializer

class BridesmaidDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bridesmaid.objects.all()
    serializer_class = BridesmaidSerializer

class GroomsmanListCreateView(generics.ListCreateAPIView):
    queryset = Groomsman.objects.all()
    serializer_class = GroomsmanSerializer

class GroomsmanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Groomsman.objects.all()
    serializer_class = GroomsmanSerializer

# Server-rendered event page for social sharing meta tags
def event_detail_page(request, slug):
    """
    If the request is from a bot/crawler (for social sharing), render the event_detail.html template with meta tags.
    Otherwise, redirect to the external wedding page with the event slug as a query parameter.
    """
    import re
    event = get_object_or_404(Event, slug=slug)
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    # List of common bot/crawler keywords
    bot_keywords = [
        'bot', 'crawl', 'slurp', 'spider', 'mediapartners', 'facebookexternalhit', 'twitterbot', 'linkedinbot', 'embedly', 'quora link preview', 'showyoubot', 'outbrain', 'pinterest', 'slackbot', 'vkshare', 'facebot', 'telegrambot', 'applebot', 'yandex', 'baiduspider', 'embed', 'discordbot', 'whatsapp', 'google', 'bing', 'duckduckbot', 'yeti', 'ahrefs', 'semrush', 'mj12bot', 'seznambot', 'sogou', 'exabot', 'ia_archiver'
    ]
    if any(bot in user_agent for bot in bot_keywords):
        return render(request, 'event_detail.html', {
            'event': event,
            'couple_names': event.get_couple_names(),
            'description': event.additional_header_text or event.header_text or '',
            'thumbnail_url': event.first_slider_image_url,
        })
    
    return redirect(f'https://savemeaseatzambia.com/wedding.html?slug={slug}')

# Example function to send reminder email to event guests

def send_event_reminder(event):
    # Get all RSVPs with emails for this event
    rsvps_with_emails = event.rsvps.filter(email__isnull=False).exclude(email='')
    
    print(f"📧 Found {rsvps_with_emails.count()} RSVPs with emails for event: {event.header_text}")
    
    if not rsvps_with_emails:
        print(f"❌ No RSVP emails found for event: {event.header_text}")
        return False
    
    subject = f"Reminder: {event.header_text or 'Your Special Event'} is coming up!"
    
    # Send personalized email to each guest
    emails_sent = 0
    for rsvp in rsvps_with_emails:
        guest_name = rsvp.full_name.split()[0] if rsvp.full_name else "Guest"  # Use first name
        
        # Professional HTML email template with personalized greeting
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Event Reminder</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .email-container {{
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 300;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .event-details {{
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                    border-left: 4px solid #667eea;
                }}
                .event-title {{
                    font-size: 24px;
                    font-weight: 600;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .event-date {{
                    font-size: 18px;
                    color: #667eea;
                    font-weight: 500;
                    margin-bottom: 10px;
                }}
                .event-venue {{
                    font-size: 16px;
                    color: #7f8c8d;
                    margin-bottom: 15px;
                }}
                .couple-names {{
                    font-size: 20px;
                    color: #2c3e50;
                    font-weight: 500;
                    margin-bottom: 15px;
                }}
                .message {{
                    font-size: 16px;
                    line-height: 1.8;
                    color: #555;
                    margin: 20px 0;
                }}
                .footer {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
                .divider {{
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #ddd, transparent);
                    margin: 20px 0;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Event Reminder</h1>
                </div>
                
                <div class="content">
                    <div class="event-details">
                        <div class="event-title">{event.header_text or 'Your Special Event'}</div>
                        <div class="event-date">📅 {event.date.strftime('%A, %B %d, %Y')}</div>
                        {f'<div class="event-venue">📍 {event.venue}</div>' if event.venue else ''}
                        {f'<div class="couple-names">💕 {event.get_couple_names()}</div>' if event.get_couple_names() else ''}
                    </div>
                    
                    <div class="message">
                        <p>Dear {guest_name},</p>
                        
                        <p>This is a friendly reminder that you're invited to a special celebration!</p>
                        
                        <div class="highlight">
                            <strong>Event Details:</strong><br>
                            • Date: {event.date.strftime('%A, %B %d, %Y')}<br>
                            {f'• Venue: {event.venue}<br>' if event.venue else ''}
                            {f'• Couple: {event.get_couple_names()}<br>' if event.get_couple_names() else ''}
                        </div>
                        
                        <p>We're looking forward to celebrating this special day with you!</p>
                        
                        <p>Best regards,<br>
                        The Event Team</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="font-size: 14px; color: #7f8c8d; text-align: center;">
                        💝 Thank you for being part of this special celebration
                    </p>
                </div>
                
                <div class="footer">
                    <p>This reminder was sent by</p>
                    <p><a href="https://savemeaseatzambia.com">savemeaseatzambia.com</a></p>
                    <p style="margin-top: 10px; font-size: 12px; color: #bdc3c7;">
                        Save Me A Seat Zambia - Making your special moments unforgettable
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version with personalized greeting
        plain_message = f"""
Dear {guest_name},

This is a friendly reminder that you're invited to a special celebration!

Event Details:
• Event: {event.header_text or 'Your Special Event'}
• Date: {event.date.strftime('%A, %B %d, %Y')}
{f'• Venue: {event.venue}' if event.venue else ''}
{f'• Couple: {event.get_couple_names()}' if event.get_couple_names() else ''}

We're looking forward to celebrating this special day with you!

Best regards,
The Event Team

---
This reminder was sent by savemeaseatzambia.com
Save Me A Seat Zambia - Making your special moments unforgettable
        """
        
        print(f"📤 Sending personalized email to: {rsvp.email} (Dear {guest_name})")
        
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [rsvp.email],
                fail_silently=False,
                html_message=html_message
            )
            emails_sent += 1
            print(f"✅ Email sent successfully to {rsvp.email}")
        except Exception as e:
            print(f"❌ Email sending failed to {rsvp.email}: {e}")
    
    print(f"📊 Total emails sent: {emails_sent}")
    return emails_sent > 0

# Test endpoint to manually send reminder emails
@csrf_exempt
def test_send_reminder(request, event_slug):
    if request.method == 'POST':
        event = get_object_or_404(Event, slug=event_slug)
        rsvp_emails = event.rsvps.filter(email__isnull=False).exclude(email='').values_list('email', flat=True)
        
        if not rsvp_emails:
            return JsonResponse({'error': 'No RSVP emails found for this event'}, status=400)
        
        try:
            success = send_event_reminder(event)
            if success:
                return JsonResponse({'success': True, 'message': f'Reminder sent to {len(rsvp_emails)} guests'})
            else:
                return JsonResponse({'error': 'Failed to send email'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Email error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Test endpoint to create sample RSVP data
@csrf_exempt
def create_test_rsvp(request, event_slug):
    if request.method == 'POST':
        event = get_object_or_404(Event, slug=event_slug)
        
        # Create test RSVP with email
        test_rsvp = RSVP.objects.create(
            event=event,
            full_name="Test Guest",
            email="your-test-email@gmail.com",  # Replace with your email for testing
            phone_number="+1234567890",
            number_of_guests=2,
            attending="yes"
        )
        
        return JsonResponse({
            'success': True, 
            'message': f'Test RSVP created for {event.header_text}',
            'rsvp_id': test_rsvp.id
        })
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Automatic reminder sending view
@csrf_exempt
def send_automatic_reminders(request):
    if request.method in ['POST', 'GET']:
        today = timezone.now().date()
        
        print(f"📅 DATE CHECK: {today}")
        
        # Find events happening in 2 days
        two_days_from_now = today + timedelta(days=2)
        events_2_days = Event.objects.filter(
            date=two_days_from_now,
            rsvps__email__isnull=False
        ).exclude(rsvps__email='').distinct()
        
        print(f"📅 Events happening in 2 days ({two_days_from_now}): {[e.header_text for e in events_2_days]}")
        
        # Find events happening today
        events_today = Event.objects.filter(
            date=today,
            rsvps__email__isnull=False
        ).exclude(rsvps__email='').distinct()
        print(f"📅 Events happening today ({today}): {[e.header_text for e in events_today]}")
        
        results = {
            'two_days_reminders': [],
            'same_day_reminders': [],
            'total_sent': 0
        }
        
        # Send 2-day reminders
        for event in events_2_days:
            print(f"🚀 Processing 2-day reminder for: {event.header_text}")
            try:
                success = send_event_reminder(event)
                if success:
                    rsvp_count = event.rsvps.filter(email__isnull=False).exclude(email='').count()
                    results['two_days_reminders'].append({
                        'event': event.header_text,
                        'date': event.date,
                        'emails_sent': rsvp_count
                    })
                    results['total_sent'] += rsvp_count
                    print(f"✅ 2-day reminder sent for {event.header_text}")
                else:
                    print(f"❌ Failed to send 2-day reminder for {event.header_text}")
            except Exception as e:
                print(f"❌ Error sending 2-day reminder for {event.header_text}: {e}")
                results['two_days_reminders'].append({
                    'event': event.header_text,
                    'error': str(e)
                })
        
        # Send same-day reminders
        for event in events_today:
            print(f"🚀 Processing same-day reminder for: {event.header_text}")
            try:
                success = send_event_reminder(event)
                if success:
                    rsvp_count = event.rsvps.filter(email__isnull=False).exclude(email='').count()
                    results['same_day_reminders'].append({
                        'event': event.header_text,
                        'date': event.date,
                        'emails_sent': rsvp_count
                    })
                    results['total_sent'] += rsvp_count
                    print(f"✅ Same-day reminder sent for {event.header_text}")
                else:
                    print(f"❌ Failed to send same-day reminder for {event.header_text}")
            except Exception as e:
                print(f"❌ Error sending same-day reminder for {event.header_text}: {e}")
                results['same_day_reminders'].append({
                    'event': event.header_text,
                    'error': str(e)
                })
        
        print(f"📊 Total emails sent: {results['total_sent']}")
        
        return JsonResponse({
            'success': True,
            'message': f'Processed reminders. Total emails sent: {results["total_sent"]}',
            'results': results
        })
    
    return JsonResponse({'error': 'Invalid method'}, status=405)
