from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Event, RSVP, Bridesmaid, Groomsman, ProgramItem,
    EventType, WeddingEvent, WeddingSliderImage, WeddingBridesmaid,
    WeddingGroomsman, WeddingGalleryImage, WeddingRSVP
)

class BridesmaidInline(admin.TabularInline):
    model = Bridesmaid
    extra = 1

class GroomsmanInline(admin.TabularInline):
    model = Groomsman
    extra = 1

class ProgramItemInline(admin.TabularInline):
    model = ProgramItem
    extra = 1

def copy_to_clipboard_link(url, text):
    return format_html(
        '<div style="display: flex; align-items: center; gap: 5px;">'
        '<a href="{0}" target="_blank">{1}</a>'
        '<button onclick="navigator.clipboard.writeText(\'{0}\');this.textContent=\'✅ Copied!\'" '
        'onmouseout="setTimeout(() => this.textContent = \'📋\', 2000)" '
        'style="background: none; border: none; cursor: pointer; font-size: 1.1em;" title="Copy to clipboard">📋</button>'
        '</div>',
        url, text
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('header_text', 'date', 'venue', 'country', 'slug', 'is_past_event', 'invitations_done', 'event_links')
    list_editable = ('slug',)  # Make slug editable in list view
    list_filter = ('is_past_event', 'invitations_done', 'date')
    readonly_fields = ('slug', 'is_past_event', 'event_api_url', 'rsvp_export_url', 'event_public_url')
    search_fields = ('header_text', 'additional_header_text', 'bride_first_name', 'groom_first_name', 'date', 'slug')
    inlines = [BridesmaidInline, GroomsmanInline, ProgramItemInline]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('header_text', 'additional_header_text', 'date', 'venue', 'country', 'invitations_done', 'slug')
        }),
        ('Important Links', {
            'fields': ('event_api_url', 'rsvp_export_url', 'event_public_url'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('center_cover_image', 'section_image', 'bride_image', 'groom_image',
                      'slider_image_1', 'slider_image_2', 'slider_image_3',
                      'slider_image_4', 'slider_image_5', 'slider_image_6'),
            'classes': ('collapse',)
        }),
    )
    
    def event_links(self, obj):
        if not obj.id:  # For new events that haven't been saved yet
            return "Save the event first to see links"
        return format_html(
            '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
            '<a href="{0}" target="_blank" class="button" style="padding: 5px 10px; background: #f0f0f0; border-radius: 4px; text-decoration: none;">🔗 View API</a>'
            '<a href="{1}" target="_blank" class="button" style="padding: 5px 10px; background: #e6f7ff; border-radius: 4px; text-decoration: none;">📊 Export RSVPs</a>'
            '<a href="{2}" target="_blank" class="button" style="padding: 5px 10px; background: #f6ffed; border-radius: 4px; text-decoration: none;">🌐 Public Page</a>'
            '</div>',
            obj.event_api_url,
            obj.rsvp_export_url,
            obj.event_public_url,
        )
    event_links.short_description = 'Quick Links'
    
    def event_api_url(self, obj):
        return copy_to_clipboard_link(obj.event_api_url, 'API Endpoint')
    event_api_url.short_description = 'API Endpoint'
    event_api_url.allow_tags = True
    
    def rsvp_export_url(self, obj):
        return copy_to_clipboard_link(obj.rsvp_export_url, 'RSVP Export')
    rsvp_export_url.short_description = 'RSVP Export'
    rsvp_export_url.allow_tags = True
    
    def event_public_url(self, obj):
        return copy_to_clipboard_link(obj.event_public_url, 'Public Page')
    event_public_url.short_description = 'Public Page'
    event_public_url.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        # Update is_past_event when saving from admin
        if obj.date:
            obj.is_past_event = timezone.now() > obj.date
        super().save_model(request, obj, form, change)

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'number_of_guests', 'attending', 'event', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'event__header_text')
    list_filter = ('attending', 'event')

# Event Type Admin
@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'display_name', 'description')
    readonly_fields = ('created_at',)
    list_editable = ('is_active',)

# Wedding Event Admin
class WeddingSliderImageInline(admin.TabularInline):
    model = WeddingSliderImage
    extra = 1
    fields = ('image', 'title', 'subtitle', 'date_text', 'order')

class WeddingBridesmaidInline(admin.TabularInline):
    model = WeddingBridesmaid
    extra = 1
    fields = ('name', 'role', 'image', 'description', 'order')

class WeddingGroomsmanInline(admin.TabularInline):
    model = WeddingGroomsman
    extra = 1
    fields = ('name', 'role', 'image', 'description', 'order')

class WeddingGalleryImageInline(admin.TabularInline):
    model = WeddingGalleryImage
    extra = 1
    fields = ('image', 'alt_text', 'is_featured', 'order')

class WeddingRSVPInline(admin.TabularInline):
    model = WeddingRSVP
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('full_name', 'email', 'phone_number', 'number_of_guests', 
              'attending', 'dietary_requirements', 'message', 'created_at')

@admin.register(WeddingEvent)
class WeddingEventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'bride_name', 'groom_name', 'event_date', 'is_published', 'is_past_event', 'rsvp_count', 'view_links')
    list_filter = ('is_published', 'is_past_event', 'event_date')
    search_fields = ('event_title', 'bride_name', 'groom_name', 'venue_name', 'slug')
    readonly_fields = ('slug', 'is_past_event', 'created_at', 'updated_at', 'event_api_url', 'event_public_url', 'rsvp_count', 'view_links')
    list_editable = ('is_published',)
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'event_type', 'event_title', 'slug', 'is_published',
                'event_date', 'event_location', 'is_past_event'
            )
        }),
        ('Color Theme', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
            'classes': ('collapse',)
        }),
        ('Couple Information', {
            'fields': (
                ('bride_name', 'bride_image', 'bride_description'),
                ('groom_name', 'groom_image', 'groom_description'),
                'countdown_title',
                'story_paragraph1', 'story_highlight', 'story_paragraph2'
            )
        }),
        ('Venue Information', {
            'fields': (
                'venue_name', 'venue_address', 'venue_description',
                'ceremony_time', 'reception_time',
                'parking_info', 'transport_info'
            )
        }),
        ('Map Settings', {
            'fields': (
                'map_method',
                'map_latitude', 'map_longitude',
                'map_place_name', 'map_formatted_address',
                'google_maps_url'
            ),
            'classes': ('collapse',)
        }),
        ('Wedding Details', {
            'fields': (
                'dress_code', 'dress_code_description',
                'accommodation_name', 'accommodation_address'
            ),
            'classes': ('collapse',)
        }),
        ('RSVP Settings', {
            'fields': ('rsvp_title', 'rsvp_subtitle', 'rsvp_background_image'),
            'classes': ('collapse',)
        }),
        ('Footer Information', {
            'fields': ('footer_logo', 'footer_text', 'footer_date_location'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'event_api_url', 'event_public_url', 'rsvp_count', 'view_links'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        WeddingSliderImageInline,
        WeddingBridesmaidInline,
        WeddingGroomsmanInline,
        WeddingGalleryImageInline,
        WeddingRSVPInline,
    ]
    
    def event_api_url(self, obj):
        if not obj.slug:
            return 'Save the event to generate URL'
        return format_html('<a href="{}" target="_blank">{}</a>', 
                         f'/api/wedding-events/{obj.slug}/',
                         f'API: {obj.event_title}')
    event_api_url.short_description = 'API URL'
    
    def event_public_url(self, obj):
        if not obj.slug:
            return 'Save the event to generate URL'
        return format_html('<a href="{}" target="_blank">{}</a>', 
                         f'/wedding2.html?slug={obj.slug}',
                         f'View {obj.event_title}')
    event_public_url.short_description = 'Public URL'
    
    def rsvp_count(self, obj):
        count = obj.rsvps.count()
        url = f'/admin/core/weddingrsvp/?wedding__id__exact={obj.id}'
        return format_html('<a href="{}" target="_blank">{} RSVPs</a>', url, count)
    rsvp_count.short_description = 'RSVPs'
    
    def view_links(self, obj):
        if not obj.slug:
            return 'Save the event first to generate links'
            
        base_url = 'https://savemeaseatzambia.com'  # Update with your domain
        wedding_url = f"{base_url}/wedding2.html?slug={obj.slug}"
        rsvp_url = f"{base_url}/api/wedding-events/{obj.slug}/rsvp/"
        rsvp_list_url = f"/admin/core/weddingrsvp/?wedding__id__exact={obj.id}"
        
        return format_html(
            '<div style="display: flex; flex-direction: column; gap: 5px;">' +
            f'<a href="{wedding_url}" target="_blank" style="display: flex; align-items: center; gap: 5px;">' +
            '   <span>🌐</span> <span>View Wedding Page</span></a>' +
            f'<a href="{rsvp_url}" target="_blank" style="display: flex; align-items: center; gap: 5px;">' +
            '   <span>📝</span> <span>RSVP API Endpoint</span></a>' +
            f'<a href="{rsvp_list_url}" style="display: flex; align-items: center; gap: 5px;">' +
            f'   <span>👥</span> <span>View RSVPs ({obj.rsvps.count()})</span></a>' +
            '</div>'
        )
    view_links.short_description = 'Quick Links'
    
    def event_api_url(self, obj):
        if not obj.slug:
            return "-"
        url = reverse('wedding-event-detail', kwargs={'slug': obj.slug})
        return format_html('<a href="{}" target="_blank">View API</a>', url)
    event_api_url.short_description = 'API URL'
    
    def event_public_url(self, obj):
        if not obj.slug:
            return "-"
        url = f"https://savemeaseat-frontend.vercel.app/wedding/{obj.slug}/"
        return format_html('<a href="{}" target="_blank">View Public Page</a>', url)
    event_public_url.short_description = 'Public URL'

# Register other wedding models with basic admin
@admin.register(WeddingSliderImage)
class WeddingSliderImageAdmin(admin.ModelAdmin):
    list_display = ('wedding', 'title', 'order')
    list_filter = ('wedding',)
    search_fields = ('title', 'wedding__event_title')
    list_editable = ('order',)

@admin.register(WeddingBridesmaid)
class WeddingBridesmaidAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'wedding', 'order')
    list_filter = ('wedding',)
    search_fields = ('name', 'role', 'wedding__event_title')
    list_editable = ('order',)

@admin.register(WeddingGroomsman)
class WeddingGroomsmanAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'wedding', 'order')
    list_filter = ('wedding',)
    search_fields = ('name', 'role', 'wedding__event_title')
    list_editable = ('order',)

@admin.register(WeddingGalleryImage)
class WeddingGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('wedding', 'alt_text', 'is_featured', 'order', 'uploaded_at')
    list_filter = ('wedding', 'is_featured')
    search_fields = ('alt_text', 'wedding__event_title')
    list_editable = ('is_featured', 'order')
    list_select_related = ('wedding',)

@admin.register(WeddingRSVP)
class WeddingRSVPAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'attending', 'number_of_guests', 'wedding', 'created_at')
    list_filter = ('attending', 'wedding')
    search_fields = ('full_name', 'email', 'phone_number', 'wedding__event_title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
