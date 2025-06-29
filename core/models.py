from django.db import models
from django.utils.text import slugify

class Event(models.Model):
    # Header Info
    header_text = models.CharField(max_length=255, blank=True, null=True)
    additional_header_text = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Images
    center_cover_image = models.ImageField(upload_to='event/cover/', blank=True, null=True)
    section_image = models.ImageField(upload_to='event/section/', blank=True, null=True)

    # Bride Info
    bride_first_name = models.CharField(max_length=100, blank=True, null=True)
    bride_last_name = models.CharField(max_length=100, blank=True, null=True)
    bride_message = models.TextField(blank=True, null=True)
    bride_image = models.ImageField(upload_to='event/bride/', blank=True, null=True)

    # Groom Info
    groom_first_name = models.CharField(max_length=100, blank=True, null=True)
    groom_last_name = models.CharField(max_length=100, blank=True, null=True)
    groom_message = models.TextField(blank=True, null=True)
    groom_image = models.ImageField(upload_to='event/groom/', blank=True, null=True)

    # Slider Images (up to 6)
    slider_image_1 = models.ImageField(upload_to='event/slider/', null=True, blank=True)
    slider_image_2 = models.ImageField(upload_to='event/slider/', null=True, blank=True)
    slider_image_3 = models.ImageField(upload_to='event/slider/', null=True, blank=True)
    slider_image_4 = models.ImageField(upload_to='event/slider/', null=True, blank=True)
    slider_image_5 = models.ImageField(upload_to='event/slider/', null=True, blank=True)
    slider_image_6 = models.ImageField(upload_to='event/slider/', null=True, blank=True)

    # Love Story
    love_story_first_meet_date = models.DateField(blank=True, null=True)
    love_story_first_meet_desc = models.TextField(blank=True, null=True)
    love_story_first_meet_image = models.ImageField(upload_to='event/love_story/', null=True, blank=True)

    love_story_first_date_date = models.DateField(blank=True, null=True)
    love_story_first_date_desc = models.TextField(blank=True, null=True)
    love_story_first_date_image = models.ImageField(upload_to='event/love_story/', null=True, blank=True)

    love_story_proposal_date = models.DateField(blank=True, null=True)
    love_story_proposal_desc = models.TextField(blank=True, null=True)
    love_story_proposal_image = models.ImageField(upload_to='event/love_story/', null=True, blank=True)

    love_story_engagement_date = models.DateField(blank=True, null=True)
    love_story_engagement_desc = models.TextField(blank=True, null=True)
    love_story_engagement_image = models.ImageField(upload_to='event/love_story/', null=True, blank=True)

    # Sweet Moments (up to 6 images)
    sweet_image_1 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)
    sweet_image_2 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)
    sweet_image_3 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)
    sweet_image_4 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)
    sweet_image_5 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)
    sweet_image_6 = models.ImageField(upload_to='event/sweet/', null=True, blank=True)

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

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
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

class RSVP(models.Model):
    ATTENDING_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    number_of_guests = models.PositiveIntegerField(default=1)
    attending = models.CharField(max_length=3, choices=ATTENDING_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} RSVP for {self.event.header_text}"
