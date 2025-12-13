from rest_framework import serializers
from .models import (
    Event, RSVP, Bridesmaid, Groomsman, ProgramItem,
    EventType, WeddingEvent, WeddingSliderImage, WeddingBridesmaid,
    WeddingGroomsman, WeddingGalleryImage, WeddingRSVP
)

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ['id', 'full_name', 'email', 'phone_number', 'number_of_guests', 'attending', 'created_at']

class BridesmaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridesmaid
        fields = ['id', 'image', 'full_name', 'role']

class GroomsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groomsman
        fields = ['id', 'image', 'full_name', 'role']

class ProgramItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramItem
        fields = ['id', 'time', 'title', 'description']

class EventSerializer(serializers.ModelSerializer):
    bridesmaids = BridesmaidSerializer(many=True, read_only=True)
    groomsmen = GroomsmanSerializer(many=True, read_only=True)
    program = ProgramItemSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'header_text', 'additional_header_text', 'date', 'venue', 'country',
            'center_cover_image', 'section_image',
            'bride_first_name', 'bride_last_name', 'bride_message', 'bride_image',
            'groom_first_name', 'groom_last_name', 'groom_message', 'groom_image',
            'slider_image_1', 'slider_image_2', 'slider_image_3',
            'slider_image_4', 'slider_image_5', 'slider_image_6',
            'love_story_first_meet_date', 'love_story_first_meet_desc', 'love_story_first_meet_image',
            'love_story_first_date_date', 'love_story_first_date_desc', 'love_story_first_date_image',
            'love_story_proposal_date', 'love_story_proposal_desc', 'love_story_proposal_image',
            'love_story_engagement_date', 'love_story_engagement_desc', 'love_story_engagement_image',
            'sweet_image_1', 'sweet_image_2', 'sweet_image_3',
            'sweet_image_4', 'sweet_image_5', 'sweet_image_6',
            'time_card1_title', 'time_card1_text1', 'time_card1_text2', 'time_card1_text3', 'time_card1_text4', 'time_card1_text5', 'time_card1_url',
            'time_card2_title', 'time_card2_text1', 'time_card2_text2', 'time_card2_text3', 'time_card2_text4', 'time_card2_text5', 'time_card2_url',
            'time_card3_title', 'time_card3_text1', 'time_card3_text2', 'time_card3_text3', 'time_card3_text4', 'time_card3_text5', 'time_card3_url',
            'main_map_url',
            'gift_1', 'gift_2', 'gift_3', 'gift_4', 'gift_5',
            'thank_you_message',
            'invitations_done',
            'slug',
            'bridesmaids',
            'groomsmen',
            'program',
        ]
        read_only_fields = ('slug',)


# ==================== WEDDING EVENT SERIALIZERS ====================

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'display_name', 'description', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class WeddingSliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingSliderImage
        fields = ['id', 'image', 'title', 'subtitle', 'date_text', 'order']


class WeddingBridesmaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingBridesmaid
        fields = ['id', 'name', 'role', 'description', 'image', 'order']


class WeddingGroomsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingGroomsman
        fields = ['id', 'name', 'role', 'description', 'image', 'order']


class WeddingGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingGalleryImage
        fields = ['id', 'image', 'alt_text', 'is_featured', 'uploaded_at', 'order']
        read_only_fields = ['uploaded_at']


class WeddingRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingRSVP
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'number_of_guests',
            'attending', 'created_at'
        ]
        read_only_fields = ['created_at']


class WeddingEventSerializer(serializers.ModelSerializer):
    """
    Main Wedding Event Serializer with nested relationships
    """
    event_type = EventTypeSerializer(read_only=True)
    event_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EventType.objects.filter(name='wedding'),
        source='event_type',
        write_only=True
    )
    slider_images = WeddingSliderImageSerializer(many=True, read_only=True)
    bridesmaids = WeddingBridesmaidSerializer(many=True, read_only=True)
    groomsmen = WeddingGroomsmanSerializer(many=True, read_only=True)
    gallery_images = WeddingGalleryImageSerializer(many=True, read_only=True)
    rsvps = WeddingRSVPSerializer(many=True, read_only=True)
    
    # Computed fields
    couple_names = serializers.ReadOnlyField()
    event_api_url = serializers.ReadOnlyField()
    event_public_url = serializers.ReadOnlyField()
    
    class Meta:
        model = WeddingEvent
        fields = [
            # System
            'id', 'event_type', 'event_type_id', 'slug', 'is_published', 'is_past_event',
            'invitations_sent', 'created_at', 'updated_at',
            
            # Basic Information
            'event_title', 'logo_text', 'event_date', 'event_location',
            
            # Color Theme
            'primary_color', 'secondary_color', 'accent_color',
            
            # Countdown
            'countdown_title',
            
            # Couple Information
            'bride_name', 'bride_image', 'bride_description',
            'groom_name', 'groom_image', 'groom_description',
            
            # Love Story
            'story_paragraph1', 'story_highlight', 'story_paragraph2',
            
            # Venue Information
            'venue_name', 'venue_description', 'venue_address',
            'ceremony_time', 'reception_time', 'parking_info', 'transport_info',
            
            # Map Location
            'map_method', 'map_latitude', 'map_longitude', 'map_place_name',
            'map_formatted_address', 'google_maps_url',
            
            # Wedding Details
            'dress_code', 'dress_code_description',
            'accommodation_name', 'accommodation_address',
            
            # RSVP Settings
            'rsvp_title', 'rsvp_subtitle', 'rsvp_background_image',
            
            # Footer
            'footer_logo', 'footer_text', 'footer_date_location',
            
            # Nested relationships
            'slider_images', 'bridesmaids', 'groomsmen', 'gallery_images', 'rsvps',
            
            # Computed fields
            'couple_names', 'event_api_url', 'event_public_url',
        ]
        read_only_fields = ['slug', 'is_past_event', 'created_at', 'updated_at']


class WeddingEventCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating wedding events
    """
    event_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EventType.objects.filter(name='wedding'),
        source='event_type'
    )
    
    class Meta:
        model = WeddingEvent
        fields = [
            'event_type_id', 'event_title', 'logo_text', 'event_date', 'event_location',
            'primary_color', 'secondary_color', 'accent_color', 'countdown_title',
            'bride_name', 'bride_image', 'bride_description',
            'groom_name', 'groom_image', 'groom_description',
            'story_paragraph1', 'story_highlight', 'story_paragraph2',
            'venue_name', 'venue_description', 'venue_address',
            'ceremony_time', 'reception_time', 'parking_info', 'transport_info',
            'map_method', 'map_latitude', 'map_longitude', 'map_place_name',
            'map_formatted_address', 'google_maps_url',
            'dress_code', 'dress_code_description',
            'accommodation_name', 'accommodation_address',
            'rsvp_title', 'rsvp_subtitle', 'rsvp_background_image',
            'footer_logo', 'footer_text', 'footer_date_location',
            'is_published',
        ]
