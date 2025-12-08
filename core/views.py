from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from .models import (
    Event, RSVP, Bridesmaid, Groomsman,
    EventType, WeddingEvent, WeddingSliderImage, WeddingBridesmaid,
    WeddingGroomsman, WeddingGalleryImage, WeddingRSVP
)
from .serializers import (
    EventSerializer, BridesmaidSerializer, GroomsmanSerializer,
    EventTypeSerializer, WeddingEventSerializer, WeddingEventCreateSerializer,
    WeddingSliderImageSerializer, WeddingBridesmaidSerializer,
    WeddingGroomsmanSerializer, WeddingGalleryImageSerializer, WeddingRSVPSerializer
)
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
                    send_event_reminder_to_guests(event)
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

def send_event_reminder_to_guests(event):
    rsvps_with_emails = event.rsvps.filter(email__isnull=False).exclude(email='')
    print(f"📧 Found {rsvps_with_emails.count()} RSVPs with emails for event: {event.header_text}")
    if not rsvps_with_emails:
        print(f"❌ No RSVP emails found for event: {event.header_text}")
        return False
    subject = f"Reminder: {event.header_text or 'Your Special Event'} is coming up!"
    emails_sent = 0
    for rsvp in rsvps_with_emails:
        guest_name = rsvp.full_name.split()[0] if rsvp.full_name else "Guest"
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

def send_wedding_reminder_to_guests(wedding_event):
    """
    Send reminder emails to all guests who RSVP'd to a wedding event
    """
    rsvps_with_emails = wedding_event.rsvps.filter(
        email__isnull=False
    ).exclude(email='')
    
    if not rsvps_with_emails:
        print(f"❌ No RSVP emails found for wedding: {wedding_event.event_title}")
        return False
        
    subject = f"Reminder: {wedding_event.event_title} is coming up!"
    emails_sent = 0
    
    for rsvp in rsvps_with_emails:
        guest_name = rsvp.full_name.split()[0] if rsvp.full_name else "Guest"
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Wedding Reminder</title>
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
                    background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%);
                    color: white;
                    padding: 30px 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .event-details {{
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                    border-left: 4px solid #8e44ad;
                }}
                .event-title {{
                    font-size: 24px;
                    font-weight: 600;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .event-date {{
                    font-size: 18px;
                    color: #8e44ad;
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
                .highlight {{
                    background-color: #f5e6ff;
                    border: 1px solid #e6ccff;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Wedding Reminder</h1>
                </div>
                <div class="content">
                    <div class="event-details">
                        <div class="event-title">{wedding_event.event_title}</div>
                        <div class="event-date">📅 {wedding_event.event_date.strftime('%A, %B %d, %Y')}</div>
                        <div class="event-venue">📍 {wedding_event.venue_name}</div>
                        <div class="couple-names">💕 {wedding_event.bride_name} & {wedding_event.groom_name}</div>
                    </div>
                    <div class="message">
                        <p>Dear {guest_name},</p>
                        <p>This is a friendly reminder about the upcoming wedding celebration!</p>
                        <div class="highlight">
                            <strong>Wedding Details:</strong><br>
                            • Date: {wedding_event.event_date.strftime('%A, %B %d, %Y')}<br>
                            • Time: {wedding_event.event_date.strftime('%I:%M %p')}<br>
                            • Venue: {wedding_event.venue_name}<br>
                            • Address: {wedding_event.venue_address}
                        </div>
                        <p>We're looking forward to celebrating with you!</p>
                        <p>Best regards,<br>
                        {wedding_event.bride_name} & {wedding_event.groom_name}</p>
                    </div>
                </div>
                <div class="footer">
                    <p>This reminder was sent by</p>
                    <p><a href="https://savemeaseatzambia.com" style="color: #9b59b6; text-decoration: none;">savemeaseatzambia.com</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
Dear {guest_name},

This is a friendly reminder about the upcoming wedding celebration!

Wedding Details:
• Couple: {wedding_event.bride_name} & {wedding_event.groom_name}
• Date: {wedding_event.event_date.strftime('%A, %B %d, %Y')}
• Time: {wedding_event.event_date.strftime('%I:%M %p')}
• Venue: {wedding_event.venue_name}
• Address: {wedding_event.venue_address}

We're looking forward to celebrating with you!

Best regards,
{wedding_event.bride_name} & {wedding_event.groom_name}
        """
        
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
            print(f"✅ Wedding reminder sent to {rsvp.email}")
        except Exception as e:
            print(f"❌ Failed to send wedding reminder to {rsvp.email}: {e}")
    
    return emails_sent > 0

@csrf_exempt
def send_event_reminder(request, event_slug):
    """
    API endpoint to trigger reminders for a specific event. Only guests (RSVPs) linked to that event will receive reminders.
    Requires a POST request with a secret key for basic security.
    """
    if request.method == 'POST':
        SECRET_KEY = 'reminder_secret_123'  # Change this to a secure value and keep it private
        data = json.loads(request.body)
        if data.get('secret_key') != SECRET_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        event = get_object_or_404(Event, slug=event_slug)
        rsvp_emails = event.rsvps.filter(email__isnull=False).exclude(email='').values_list('email', flat=True)
        if not rsvp_emails:
            return JsonResponse({'error': 'No RSVP emails found for this event'}, status=400)
        try:
            success = send_event_reminder_to_guests(event)
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
                success = send_event_reminder_to_guests(event)
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
                success = send_event_reminder_to_guests(event)
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


# ==================== WEDDING EVENT API VIEWS ====================

class EventTypeListView(generics.ListAPIView):
    """
    List all event types (Wedding, Birthday, Corporate)
    GET /api/event-types/
    """
    queryset = EventType.objects.filter(is_active=True)
    serializer_class = EventTypeSerializer


class WeddingEventListCreateView(generics.ListCreateAPIView):
    """
    List all wedding events or create a new one
    GET /api/wedding-events/
    POST /api/wedding-events/
    """
    queryset = WeddingEvent.objects.all().order_by('-event_date')
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Allow unauthenticated access
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WeddingEventCreateSerializer
        return WeddingEventSerializer
    
    def create(self, request, *args, **kwargs):
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info("Received wedding event creation request")
            logger.debug(f"Request data: {request.data}")
            
            # Ensure event_type exists
            try:
                event_type = EventType.objects.get(name='wedding')
                logger.debug(f"Found event_type: {event_type}")
            except EventType.DoesNotExist:
                error_msg = 'Wedding event type does not exist. Please create a Wedding event type first.'
                logger.error(error_msg)
                return Response(
                    {
                        'error': error_msg,
                        'solution': 'Create an EventType with name="wedding" in the admin interface or run the initialize_event_types management command.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Get the serializer with the request data
            serializer = self.get_serializer(data=request.data)
            
            # Validate the data
            if not serializer.is_valid():
                return Response(
                    {
                        'error': 'Validation failed',
                        'details': serializer.errors,
                        'required_fields': [
                            'event_title',
                            'event_date',
                            'event_location',
                            'bride_name',
                            'groom_name',
                            'venue_name',
                            'ceremony_time'
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save the event
            event = serializer.save(event_type=event_type)
            
            # Return success response with the created event data
            return Response(
                {
                    'message': 'Wedding event created successfully',
                    'id': event.id,
                    'slug': event.slug,
                    'event_title': event.event_title,
                    'event_date': event.event_date
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            # Log the full traceback
            error_trace = traceback.format_exc()
            logger.error(f"Error creating wedding event: {str(e)}\n{error_trace}")
            
            # Return detailed error response
            return Response(
                {
                    'error': 'An error occurred while creating the wedding event',
                    'details': str(e),
                    'traceback': error_trace if settings.DEBUG else None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WeddingEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a wedding event
    GET /api/wedding-events/<slug>/
    PUT /api/wedding-events/<slug>/
    PATCH /api/wedding-events/<slug>/
    DELETE /api/wedding-events/<slug>/
    """
    queryset = WeddingEvent.objects.all()
    serializer_class = WeddingEventSerializer
    lookup_field = 'slug'
    parser_classes = (MultiPartParser, FormParser)


# ===== WEDDING SLIDER IMAGES =====

class WeddingSliderImageListCreateView(generics.ListCreateAPIView):
    """
    List or create slider images for a wedding
    GET /api/wedding-events/<slug>/sliders/
    POST /api/wedding-events/<slug>/sliders/
    """
    serializer_class = WeddingSliderImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        wedding_slug = self.kwargs.get('wedding_slug')
        return WeddingSliderImage.objects.filter(wedding__slug=wedding_slug).order_by('order')
    
    def perform_create(self, serializer):
        wedding_slug = self.kwargs.get('wedding_slug')
        wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
        serializer.save(wedding=wedding)


class WeddingSliderImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a slider image
    GET /api/wedding-sliders/<id>/
    PUT /api/wedding-sliders/<id>/
    DELETE /api/wedding-sliders/<id>/
    """
    queryset = WeddingSliderImage.objects.all()
    serializer_class = WeddingSliderImageSerializer
    parser_classes = (MultiPartParser, FormParser)


# ===== WEDDING BRIDESMAIDS =====

class WeddingBridesmaidListCreateView(generics.ListCreateAPIView):
    """
    List or create bridesmaids for a wedding
    GET /api/wedding-events/<slug>/bridesmaids/
    POST /api/wedding-events/<slug>/bridesmaids/
    """
    serializer_class = WeddingBridesmaidSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        wedding_slug = self.kwargs.get('wedding_slug')
        return WeddingBridesmaid.objects.filter(wedding__slug=wedding_slug).order_by('order')
    
    def perform_create(self, serializer):
        wedding_slug = self.kwargs.get('wedding_slug')
        wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
        serializer.save(wedding=wedding)


class WeddingBridesmaidDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a bridesmaid
    GET /api/wedding-bridesmaids/<id>/
    PUT /api/wedding-bridesmaids/<id>/
    DELETE /api/wedding-bridesmaids/<id>/
    """
    queryset = WeddingBridesmaid.objects.all()
    serializer_class = WeddingBridesmaidSerializer
    parser_classes = (MultiPartParser, FormParser)


# ===== WEDDING GROOMSMEN =====

class WeddingGroomsmanListCreateView(generics.ListCreateAPIView):
    """
    List or create groomsmen for a wedding
    GET /api/wedding-events/<slug>/groomsmen/
    POST /api/wedding-events/<slug>/groomsmen/
    """
    serializer_class = WeddingGroomsmanSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        wedding_slug = self.kwargs.get('wedding_slug')
        return WeddingGroomsman.objects.filter(wedding__slug=wedding_slug).order_by('order')
    
    def perform_create(self, serializer):
        wedding_slug = self.kwargs.get('wedding_slug')
        wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
        serializer.save(wedding=wedding)


class WeddingGroomsmanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a groomsman
    GET /api/wedding-groomsmen/<id>/
    PUT /api/wedding-groomsmen/<id>/
    DELETE /api/wedding-groomsmen/<id>/
    """
    queryset = WeddingGroomsman.objects.all()
    serializer_class = WeddingGroomsmanSerializer
    parser_classes = (MultiPartParser, FormParser)


# ===== WEDDING GALLERY =====

class WeddingGalleryImageListCreateView(generics.ListCreateAPIView):
    """
    List or create gallery images for a wedding
    GET /api/wedding-events/<slug>/gallery/
    POST /api/wedding-events/<slug>/gallery/
    """
    serializer_class = WeddingGalleryImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        wedding_slug = self.kwargs.get('wedding_slug')
        return WeddingGalleryImage.objects.filter(wedding__slug=wedding_slug).order_by('order', '-uploaded_at')
    
    def perform_create(self, serializer):
        wedding_slug = self.kwargs.get('wedding_slug')
        wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
        serializer.save(wedding=wedding)


class WeddingGalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a gallery image
    GET /api/wedding-gallery/<id>/
    PUT /api/wedding-gallery/<id>/
    DELETE /api/wedding-gallery/<id>/
    """
    queryset = WeddingGalleryImage.objects.all()
    serializer_class = WeddingGalleryImageSerializer
    parser_classes = (MultiPartParser, FormParser)


# ===== WEDDING RSVP =====

@csrf_exempt
def wedding_page(request):
    """
    Handle dynamic wedding pages with format: /wedding2.html?slug=bride-groom-YYYY-MM-DD
    """
    slug = request.GET.get('slug')
    if not slug:
        return HttpResponseBadRequest("Missing slug parameter")
    
    try:
        # Extract date from slug (last part after last dash)
        date_part = slug.split('-')[-3:]
        if len(date_part) != 3:
            raise ValueError("Invalid date format in slug")
            
        event_date = f"{date_part[0]}-{date_part[1]}-{date_part[2]}"
        
        # Find wedding by date and names
        wedding = WeddingEvent.objects.get(
            event_date=event_date,
            slug__icontains=slug.rsplit('-', 3)[0]  # Match the name part
        )
        
        # Get related data
        sliders = wedding.slider_images.all()
        bridesmaids = wedding.bridesmaids.all()
        groomsmen = wedding.groomsmen.all()
        gallery = wedding.gallery_images.all()
        
        context = {
            'wedding': wedding,
            'sliders': sliders,
            'bridesmaids': bridesmaids,
            'groomsmen': groomsmen,
            'gallery': gallery,
        }
        
        return render(request, 'wedding2.html', context)
        
    except (ValueError, WeddingEvent.DoesNotExist) as e:
        return HttpResponseNotFound("Wedding not found")


def wedding_rsvp_submit(request, wedding_slug):
    """
    Submit RSVP for a wedding event
    POST /api/wedding-events/<slug>/rsvp/
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
            
            rsvp = WeddingRSVP.objects.create(
                wedding=wedding,
                full_name=data.get('full_name'),
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                number_of_guests=data.get('number_of_guests', 1),
                attending=data.get('attending'),
                dietary_requirements=data.get('dietary_requirements', ''),
                message=data.get('message', '')
            )
            
            return JsonResponse({
                'success': True,
                'id': rsvp.id,
                'message': 'RSVP submitted successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


class WeddingRSVPListView(generics.ListAPIView):
    """
    List all RSVPs for a wedding (admin only)
    GET /api/wedding-events/<slug>/rsvps/
    """
    serializer_class = WeddingRSVPSerializer
    
    def get_queryset(self):
        wedding_slug = self.kwargs.get('wedding_slug')
        return WeddingRSVP.objects.filter(wedding__slug=wedding_slug).order_by('-created_at')


def wedding_rsvp_export_csv(request, wedding_slug):
    """
    Export RSVPs to CSV
    GET /api/wedding-events/<slug>/rsvp/export/
    """
    wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
    rsvps = wedding.rsvps.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="wedding_rsvp_{wedding_slug}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Full Name', 'Email', 'Phone Number', 'Number of Guests',
        'Attending', 'Dietary Requirements', 'Message', 'Created At'
    ])
    
    for rsvp in rsvps:
        writer.writerow([
            rsvp.full_name,
            rsvp.email or '',
            rsvp.phone_number or '',
            rsvp.number_of_guests,
            rsvp.get_attending_display(),
            rsvp.dietary_requirements or '',
            rsvp.message or '',
            rsvp.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response
