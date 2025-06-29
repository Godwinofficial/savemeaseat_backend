from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('header_text', 'additional_header_text', 'date', 'venue', 'country', 'slug')
    readonly_fields = ('slug',)
    search_fields = ('header_text', 'additional_header_text', 'bride_first_name', 'groom_first_name', 'date', 'slug')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'number_of_guests', 'attending', 'event', 'created_at')
    search_fields = ('full_name', 'phone_number', 'event__header_text')
    list_filter = ('attending', 'event')

