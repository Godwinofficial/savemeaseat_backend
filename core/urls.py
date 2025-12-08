from django.urls import path
from .views import (
    EventListCreateView, EventRetrieveUpdateDestroyView,
    BridesmaidListCreateView, BridesmaidDetailView,
    GroomsmanListCreateView, GroomsmanDetailView,
    event_detail_page,
    # Wedding Event Views
    EventTypeListView, WeddingEventListCreateView, WeddingEventDetailView,
    WeddingSliderImageListCreateView, WeddingSliderImageDetailView,
    WeddingBridesmaidListCreateView, WeddingBridesmaidDetailView,
    WeddingGroomsmanListCreateView, WeddingGroomsmanDetailView,
    WeddingGalleryImageListCreateView, WeddingGalleryImageDetailView,
    WeddingRSVPListView
)
from . import views
from .wedding_preview import wedding_event_preview

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<slug:slug>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<slug:event_slug>/rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('events/<slug:event_slug>/rsvp/export/', views.export_rsvp_csv, name='export_rsvp_csv'),
    path('events/<slug:event_slug>/send-reminder/', views.send_event_reminder, name='send_event_reminder'),
    path('events/<slug:event_slug>/create-test-rsvp/', views.create_test_rsvp, name='create_test_rsvp'),
    path('send-reminders/', views.send_automatic_reminders, name='send_automatic_reminders'),
    path('event/<slug:slug>/', event_detail_page, name='event-detail-page'),
    # (Removed legacy Event gallery endpoints; use Wedding gallery endpoints instead)
    
    # ==================== WEDDING EVENT ENDPOINTS ====================
    # Event Types
    path('event-types/', EventTypeListView.as_view(), name='event-type-list'),
    
    # Wedding Events
    path('wedding-events/', WeddingEventListCreateView.as_view(), name='wedding-event-list-create'),
    path('wedding-events/<slug:slug>/', WeddingEventDetailView.as_view(), name='wedding-event-detail'),
    path('wedding2.html', views.wedding_page, name='wedding-page'),  # New dynamic wedding page
    path('wedding-events/<slug:wedding_slug>/preview/', wedding_event_preview, name='wedding-event-preview'),
    
    # Wedding Slider Images
    path('wedding-events/<slug:wedding_slug>/sliders/', WeddingSliderImageListCreateView.as_view(), name='wedding-slider-list-create'),
    path('wedding-sliders/<int:pk>/', WeddingSliderImageDetailView.as_view(), name='wedding-slider-detail'),
    
    # Wedding Bridesmaids
    path('wedding-events/<slug:wedding_slug>/bridesmaids/', WeddingBridesmaidListCreateView.as_view(), name='wedding-bridesmaid-list-create'),
    path('wedding-bridesmaids/<int:pk>/', WeddingBridesmaidDetailView.as_view(), name='wedding-bridesmaid-detail'),
    
    # Wedding Groomsmen
    path('wedding-events/<slug:wedding_slug>/groomsmen/', WeddingGroomsmanListCreateView.as_view(), name='wedding-groomsman-list-create'),
    path('wedding-groomsmen/<int:pk>/', WeddingGroomsmanDetailView.as_view(), name='wedding-groomsman-detail'),
    
    # Wedding Gallery
    path('wedding-events/<slug:wedding_slug>/gallery/', WeddingGalleryImageListCreateView.as_view(), name='wedding-gallery-list-create'),
    path('wedding-gallery/<int:pk>/', WeddingGalleryImageDetailView.as_view(), name='wedding-gallery-detail'),
    
    # Wedding RSVP
    path('wedding-events/<slug:wedding_slug>/rsvp/', views.wedding_rsvp_submit, name='wedding-rsvp-submit'),
    path('wedding-events/<slug:wedding_slug>/rsvps/', WeddingRSVPListView.as_view(), name='wedding-rsvp-list'),
    path('wedding-events/<slug:wedding_slug>/rsvp/export/', views.wedding_rsvp_export_csv, name='wedding-rsvp-export'),
    
    # Original Event Bridesmaids/Groomsmen
    path('bridesmaids/', BridesmaidListCreateView.as_view(), name='bridesmaid-list-create'),
    path('bridesmaids/<int:pk>/', BridesmaidDetailView.as_view(), name='bridesmaid-detail'),
    path('groomsmen/', GroomsmanListCreateView.as_view(), name='groomsman-list-create'),
    path('groomsmen/<int:pk>/', GroomsmanDetailView.as_view(), name='groomsman-detail'),
]
