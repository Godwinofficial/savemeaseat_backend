from django.contrib import admin
from .models import Event, RSVP, Bridesmaid, Groomsman, ProgramItem

class BridesmaidInline(admin.TabularInline):
    model = Bridesmaid
    extra = 1

class GroomsmanInline(admin.TabularInline):
    model = Groomsman
    extra = 1

class ProgramItemInline(admin.TabularInline):
    model = ProgramItem
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('header_text', 'additional_header_text', 'date', 'venue', 'country', 'slug')
    readonly_fields = ('slug',)
    search_fields = ('header_text', 'additional_header_text', 'bride_first_name', 'groom_first_name', 'date', 'slug')
    inlines = [BridesmaidInline, GroomsmanInline, ProgramItemInline]

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'number_of_guests', 'attending', 'event', 'created_at')
    search_fields = ('full_name', 'phone_number', 'event__header_text')
    list_filter = ('attending', 'event')

admin.site.register(Bridesmaid)
admin.site.register(Groomsman)
admin.site.register(ProgramItem)

