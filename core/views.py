from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Event, RSVP, Bridesmaid, Groomsman
from .serializers import EventSerializer, BridesmaidSerializer, GroomsmanSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv

# Create your views here.

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
            phone_number=data.get('phone_number'),
            number_of_guests=data.get('number_of_guests', 1),
            attending=data.get('attending')
        )
        return JsonResponse({'success': True, 'id': rsvp.id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def export_rsvp_csv(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    rsvps = event.rsvps.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="rsvp_{event_slug}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Phone Number', 'Number of Guests', 'Attending', 'Created At'])
    for rsvp in rsvps:
        writer.writerow([rsvp.full_name, rsvp.phone_number, rsvp.number_of_guests, rsvp.attending, rsvp.created_at])
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
