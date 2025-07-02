from rest_framework import serializers
from .models import Event, RSVP, Bridesmaid, Groomsman, ProgramItem

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
            'slug',
            'bridesmaids',
            'groomsmen',
            'program',
        ]
        read_only_fields = ('slug',)
