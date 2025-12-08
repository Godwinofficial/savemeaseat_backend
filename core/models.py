from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class Event(models.Model):
    # Header Info
    header_text = models.CharField(max_length=255, blank=True, null=True)
    additional_header_text = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)  # Changed from DateField to DateTimeField
    venue = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Images
    center_cover_image = CloudinaryField('event/cover/', use_filename=True, unique_filename=True, blank=True, null=True)
    section_image = CloudinaryField('event/section/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Bride Info
    bride_first_name = models.CharField(max_length=100, blank=True, null=True)
    bride_last_name = models.CharField(max_length=100, blank=True, null=True)
    bride_message = models.TextField(blank=True, null=True)
    bride_image = CloudinaryField('event/bride/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Groom Infor
    groom_first_name = models.CharField(max_length=100, blank=True, null=True)
    groom_last_name = models.CharField(max_length=100, blank=True, null=True)
    groom_message = models.TextField(blank=True, null=True)
    groom_image = CloudinaryField('event/groom/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Slider Images (up to 6)
    slider_image_1 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)
    slider_image_2 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)
    slider_image_3 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)
    slider_image_4 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)
    slider_image_5 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)
    slider_image_6 = CloudinaryField('event/slider/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Love Story
    love_story_first_meet_date = models.DateField(blank=True, null=True)
    love_story_first_meet_desc = models.TextField(blank=True, null=True)
    love_story_first_meet_image = CloudinaryField('event/love_story/', use_filename=True, unique_filename=True, blank=True, null=True)

    love_story_first_date_date = models.DateField(blank=True, null=True)
    love_story_first_date_desc = models.TextField(blank=True, null=True)
    love_story_first_date_image = CloudinaryField('event/love_story/', use_filename=True, unique_filename=True, blank=True, null=True)

    love_story_proposal_date = models.DateField(blank=True, null=True)
    love_story_proposal_desc = models.TextField(blank=True, null=True)
    love_story_proposal_image = CloudinaryField('event/love_story/', use_filename=True, unique_filename=True, blank=True, null=True)

    love_story_engagement_date = models.DateField(blank=True, null=True)
    love_story_engagement_desc = models.TextField(blank=True, null=True)
    love_story_engagement_image = CloudinaryField('event/love_story/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Sweet Moments (up to 6 images)
    sweet_image_1 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)
    sweet_image_2 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)
    sweet_image_3 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)
    sweet_image_4 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)
    sweet_image_5 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)
    sweet_image_6 = CloudinaryField('event/sweet/', use_filename=True, unique_filename=True, blank=True, null=True)

    # Time and Place Cards (3 cards)
    time_card1_title = models.CharField(max_length=100, blank=True, null=True)
    time_card1_text1 = models.CharField(max_length=255, blank=True, null=True)
    time_card1_text2 = models.CharField(max_length=255, blank=True, null=True)
    time_card1_text3 = models.CharField(max_length=255, blank=True, null=True)
    time_card1_text4 = models.CharField(max_length=255, blank=True, null=True)
    time_card1_text5 = models.CharField(max_length=255, blank=True, null=True)
    time_card1_url = models.URLField(blank=True, null=True)

    time_card2_title = models.CharField(max_length=100, blank=True, null=True)
    time_card2_text1 = models.CharField(max_length=255, blank=True, null=True)
    time_card2_text2 = models.CharField(max_length=255, blank=True, null=True)
    time_card2_text3 = models.CharField(max_length=255, blank=True, null=True)
    time_card2_text4 = models.CharField(max_length=255, blank=True, null=True)
    time_card2_text5 = models.CharField(max_length=255, blank=True, null=True)
    time_card2_url = models.URLField(blank=True, null=True)

    time_card3_title = models.CharField(max_length=100, blank=True, null=True)
    time_card3_text1 = models.CharField(max_length=255, blank=True, null=True)
    time_card3_text2 = models.CharField(max_length=255, blank=True, null=True)
    time_card3_text3 = models.CharField(max_length=255, blank=True, null=True)
    time_card3_text4 = models.CharField(max_length=255, blank=True, null=True)
    time_card3_text5 = models.CharField(max_length=255, blank=True, null=True)
    time_card3_url = models.URLField(blank=True, null=True)

    # Main Map
    main_map_url = models.URLField(max_length=1000, blank=True, null=True)

    # Gifts & Contributions
    gift_1 = models.CharField(max_length=255, blank=True, null=True)
    gift_2 = models.CharField(max_length=255, blank=True, null=True)
    gift_3 = models.CharField(max_length=255, blank=True, null=True)
    gift_4 = models.CharField(max_length=255, blank=True, null=True)
    gift_5 = models.CharField(max_length=255, blank=True, null=True)

    thank_you_message = models.TextField(default="Thank you for your love and support!", blank=True, null=True)

    # When true, invitations are considered completed and further invitation actions should be blocked.
    invitations_done = models.BooleanField(default=False, help_text="When true, invitations are marked done and further invitations should be blocked.")
    is_past_event = models.BooleanField(default=False, help_text='Automatically set to True if event date is in the past')

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Update is_past_event status
        if self.date:
            self.is_past_event = timezone.now() > self.date
            
        if not self.slug:
            slug_base = f"{self.bride_first_name}-{self.groom_first_name}-{self.date}"
            self.slug = slugify(slug_base)
            # Ensure uniqueness
            counter = 1
            orig_slug = self.slug
            while Event.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.header_text

    def get_couple_names(self):
        return f"{self.bride_first_name or ''} & {self.groom_first_name or ''}".strip()

    @property
    def first_slider_image_url(self):
        slider_images = [
            self.slider_image_1,
            self.slider_image_2,
            self.slider_image_3,
            self.slider_image_4,
            self.slider_image_5,
            self.slider_image_6,
        ]
        return next((img.url for img in slider_images if img), '/static/default-thumbnail.jpg')
    
    @property
    def event_api_url(self):
        if not hasattr(self, 'slug') or not self.slug:
            return "#"
        return f"https://savemeaseat-backend.onrender.com/api/events/{self.slug}/"
    
    @property
    def rsvp_export_url(self):
        if not hasattr(self, 'slug') or not self.slug:
            return "#"
        return f"https://savemeaseat-backend.onrender.com/api/events/{self.slug}/rsvp/export/"
    
    @property
    def event_public_url(self):
        if not hasattr(self, 'slug') or not self.slug:
            return "#"
        return f"https://savemeaseat-frontend.vercel.app/event/{self.slug}/"

# Removed automatic reminder sending on event date change. Reminders are now only triggered by the frontend.
# (Deleted @receiver(post_save, sender=Event) and send_reminder_on_date_change)

class RSVP(models.Model):
    ATTENDING_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    number_of_guests = models.PositiveIntegerField(default=1)
    attending = models.CharField(max_length=3, choices=ATTENDING_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} RSVP for {self.event.header_text}"

class Bridesmaid(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bridesmaids')
    image = CloudinaryField('event/bridesmaids/', use_filename=True, unique_filename=True, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Groomsman(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='groomsmen')
    image = CloudinaryField('event/groomsmen/', use_filename=True, unique_filename=True, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class ProgramItem(models.Model):
    event = models.ForeignKey(Event, related_name='program', on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.time} - {self.title}"


# ==================== NEW EVENT TYPE SYSTEM ====================

class EventType(models.Model):
    """
    Event Type Model - Defines different types of events
    (Wedding, Birthday, Corporate Event)
    """
    EVENT_TYPE_CHOICES = (
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
    )
    
    name = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'
        ordering = ['display_name']


class WeddingEvent(models.Model):
    """
    Wedding Event Model - Comprehensive wedding event management
    Following the complete wedding documentation specifications
    """
    # Event Type Link
    event_type = models.ForeignKey(
        EventType, 
        on_delete=models.PROTECT, 
        related_name='wedding_events',
        limit_choices_to={'name': 'wedding'}
    )
    
    # ===== 1. BASIC INFORMATION =====
    event_title = models.CharField(
        max_length=255, 
        help_text='Main wedding title (e.g., "Sophia & Alexander")'
    )
    logo_text = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='Logo/Initials (e.g., "S & A")'
    )
    event_date = models.DateTimeField(help_text='Wedding date and time')
    event_location = models.CharField(
        max_length=200, 
        help_text='City/location name (e.g., "Lusaka, Zambia")'
    )
    
    # ===== 2. COLOR THEME =====
    primary_color = models.CharField(
        max_length=7, 
        default='#f8f5f2',
        help_text='Primary background color (hex format)'
    )
    secondary_color = models.CharField(
        max_length=7, 
        default='#e8d5c4',
        help_text='Secondary elements color (hex format)'
    )
    accent_color = models.CharField(
        max_length=7, 
        default='#c8a97e',
        help_text='Highlights and accents color (hex format)'
    )
    
    # ===== 3. COUNTDOWN SECTION =====
    countdown_title = models.CharField(
        max_length=255,
        default='Counting Down to Our Special Day',
        blank=True,
        null=True
    )
    
    # ===== 4. COUPLE INFORMATION =====
    # Bride
    bride_name = models.CharField(max_length=100, help_text='Bride full name')
    bride_image = CloudinaryField(
        'wedding/bride/', 
        use_filename=True, 
        unique_filename=True,
        help_text='Bride photo upload'
    )
    bride_description = models.TextField(
        blank=True, 
        null=True,
        help_text='Bride description/bio'
    )
    
    # Groom
    groom_name = models.CharField(max_length=100, help_text='Groom full name')
    groom_image = CloudinaryField(
        'wedding/groom/', 
        use_filename=True, 
        unique_filename=True,
        help_text='Groom photo upload'
    )
    groom_description = models.TextField(
        blank=True, 
        null=True,
        help_text='Groom description/bio'
    )
    
    # ===== 5. LOVE STORY =====
    story_paragraph1 = models.TextField(
        blank=True, 
        null=True,
        help_text='Opening story paragraph'
    )
    story_highlight = models.TextField(
        blank=True, 
        null=True,
        help_text='Special quote or highlight'
    )
    story_paragraph2 = models.TextField(
        blank=True, 
        null=True,
        help_text='Continuation of story'
    )
    
    # ===== 6. VENUE INFORMATION =====
    venue_name = models.CharField(
        max_length=255,
        help_text='Name of venue (e.g., "The Glass House")'
    )
    venue_description = models.TextField(
        blank=True, 
        null=True,
        help_text='Detailed venue description'
    )
    venue_address = models.TextField(help_text='Full venue address')
    ceremony_time = models.TimeField(help_text='Ceremony start time')
    reception_time = models.TimeField(
        blank=True, 
        null=True,
        help_text='Reception start time'
    )
    parking_info = models.TextField(
        blank=True, 
        null=True,
        help_text='Parking details and instructions'
    )
    transport_info = models.TextField(
        blank=True, 
        null=True,
        help_text='Public transport information'
    )
    
    # ===== 7. MAP LOCATION (Dual Options) =====
    map_method = models.CharField(
        max_length=20,
        choices=[
            ('search', 'Interactive Search (OpenStreetMap)'),
            ('google', 'Google Maps Embed')
        ],
        default='search',
        help_text='Choose map display method'
    )
    
    # OpenStreetMap data
    map_latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        blank=True, 
        null=True,
        help_text='Latitude coordinate'
    )
    map_longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        blank=True, 
        null=True,
        help_text='Longitude coordinate'
    )
    map_place_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text='Place name from map search'
    )
    map_formatted_address = models.TextField(
        blank=True, 
        null=True,
        help_text='Formatted address from geocoding'
    )
    
    # Google Maps embed URL
    google_maps_url = models.URLField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='Google Maps embed URL'
    )
    
    # ===== 8. WEDDING DETAILS =====
    dress_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Dress code (e.g., "Formal Attire", "Black Tie")'
    )
    dress_code_description = models.TextField(
        blank=True,
        null=True,
        help_text='Additional dress code details'
    )
    accommodation_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Recommended hotel name'
    )
    accommodation_address = models.TextField(
        blank=True,
        null=True,
        help_text='Hotel address'
    )
    
    # ===== 9. RSVP SETTINGS =====
    rsvp_title = models.CharField(
        max_length=100,
        default='RSVP',
        blank=True,
        null=True
    )
    rsvp_subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='e.g., "Kindly respond by September 1st"'
    )
    rsvp_background_image = CloudinaryField(
        'wedding/rsvp/',
        use_filename=True,
        unique_filename=True,
        blank=True,
        null=True,
        help_text='RSVP section background image'
    )
    
    # ===== 10. FOOTER INFORMATION =====
    footer_logo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Footer logo text'
    )
    footer_text = models.TextField(
        blank=True,
        null=True,
        help_text='Footer message text'
    )
    footer_date_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Date and location summary for footer'
    )
    
    # ===== SYSTEM FIELDS =====
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    is_published = models.BooleanField(default=False, help_text='Publish wedding website')
    is_past_event = models.BooleanField(
        default=False,
        help_text='Automatically set to True if event date is in the past'
    )
    invitations_sent = models.BooleanField(
        default=False,
        help_text='Track if invitations have been sent'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Update is_past_event status
        if self.event_date:
            self.is_past_event = timezone.now() > self.event_date
        
        # Generate slug if not set
        if not self.slug:
            # Format: bride-groom-yyyy-mm-dd
            slug_base = f"{self.bride_name}-{self.groom_name}-{self.event_date.strftime('%Y-%m-%d')}"
            self.slug = slugify(slug_base)
            
            # Ensure uniqueness
            counter = 1
            orig_slug = self.slug
            while WeddingEvent.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.event_title
    
    @property
    def couple_names(self):
        return f"{self.bride_name} & {self.groom_name}"
    
    @property
    def event_api_url(self):
        if not self.slug:
            return "#"
        return f"https://savemeaseat-backend.onrender.com/api/wedding/{self.slug}/"
    
    @property
    def event_public_url(self):
        if not self.slug:
            return "#"
        return f"https://savemeaseatzambia.com/wedding/{self.slug}/"
    
    @property
    def event_preview_url(self):
        if not self.slug:
            return "#"
        return f"https://savemeaseat-backend.onrender.com/api/wedding-events/{self.slug}/"
    
    class Meta:
        verbose_name = 'Wedding Event'
        verbose_name_plural = 'Wedding Events'
        ordering = ['-event_date']


class WeddingSliderImage(models.Model):
    """
    Hero Slider Images for Wedding Events
    Repeatable section - multiple slides per wedding
    """
    wedding = models.ForeignKey(
        WeddingEvent,
        on_delete=models.CASCADE,
        related_name='slider_images'
    )
    image = CloudinaryField(
        'wedding/slider/',
        use_filename=True,
        unique_filename=True,
        help_text='Slide image upload'
    )
    title = models.CharField(
        max_length=255,
        help_text='Main heading for slide'
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Secondary text'
    )
    date_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Date/location text for slide'
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    def __str__(self):
        return f"{self.wedding.event_title} - Slide: {self.title}"
    
    class Meta:
        verbose_name = 'Wedding Slider Image'
        verbose_name_plural = 'Wedding Slider Images'
        ordering = ['order', 'id']


class WeddingBridesmaid(models.Model):
    """
    Bridesmaids for Wedding Events
    Repeatable section - multiple bridesmaids per wedding
    """
    wedding = models.ForeignKey(
        WeddingEvent,
        on_delete=models.CASCADE,
        related_name='bridesmaids'
    )
    name = models.CharField(max_length=255, help_text='Full name')
    role = models.CharField(
        max_length=100,
        help_text='Position (e.g., "Maid of Honor", "Bridesmaid")'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Relationship description'
    )
    image = CloudinaryField(
        'wedding/bridesmaids/',
        use_filename=True,
        unique_filename=True,
        help_text='Bridesmaid photo upload'
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    class Meta:
        verbose_name = 'Wedding Bridesmaid'
        verbose_name_plural = 'Wedding Bridesmaids'
        ordering = ['order', 'id']


class WeddingGroomsman(models.Model):
    """
    Groomsmen for Wedding Events
    Repeatable section - multiple groomsmen per wedding
    """
    wedding = models.ForeignKey(
        WeddingEvent,
        on_delete=models.CASCADE,
        related_name='groomsmen'
    )
    name = models.CharField(max_length=255, help_text='Full name')
    role = models.CharField(
        max_length=100,
        help_text='Position (e.g., "Best Man", "Groomsman")'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Relationship description'
    )
    image = CloudinaryField(
        'wedding/groomsmen/',
        use_filename=True,
        unique_filename=True,
        help_text='Groomsman photo upload'
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    class Meta:
        verbose_name = 'Wedding Groomsman'
        verbose_name_plural = 'Wedding Groomsmen'
        ordering = ['order', 'id']


class WeddingGalleryImage(models.Model):
    """
    Gallery Images for Wedding Events
    Repeatable section - multiple gallery images per wedding
    """
    wedding = models.ForeignKey(
        WeddingEvent,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = CloudinaryField(
        'wedding/gallery/',
        use_filename=True,
        unique_filename=True,
        help_text='Gallery image upload'
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Image description for accessibility'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Mark as featured image'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    def __str__(self):
        return f"{self.wedding.event_title} - Gallery Image {self.id}"
    
    class Meta:
        verbose_name = 'Wedding Gallery Image'
        verbose_name_plural = 'Wedding Gallery Images'
        ordering = ['order', '-uploaded_at']


class WeddingRSVP(models.Model):
    """
    RSVP responses for Wedding Events
    """
    ATTENDING_CHOICES = (
        ('yes', 'Yes, I will attend'),
        ('no', 'No, I cannot attend'),
        ('maybe', 'Maybe'),
    )
    
    wedding = models.ForeignKey(
        WeddingEvent,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    number_of_guests = models.PositiveIntegerField(default=1)
    attending = models.CharField(max_length=10, choices=ATTENDING_CHOICES)
    dietary_requirements = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True, help_text='Special message or notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.attending} ({self.wedding.event_title})"
    
    class Meta:
        verbose_name = 'Wedding RSVP'
        verbose_name_plural = 'Wedding RSVPs'
        ordering = ['-created_at']
