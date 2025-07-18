from django.urls import path
from .views import EventListCreateView, EventRetrieveUpdateDestroyView
from .views import BridesmaidListCreateView, BridesmaidDetailView, GroomsmanListCreateView, GroomsmanDetailView
from . import views
from .views import event_detail_page

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<slug:slug>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<slug:event_slug>/rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('events/<slug:event_slug>/rsvp/export/', views.export_rsvp_csv, name='export_rsvp_csv'),
    path('events/<slug:event_slug>/send-reminder/', views.send_event_reminder, name='send_event_reminder'),
    path('events/<slug:event_slug>/create-test-rsvp/', views.create_test_rsvp, name='create_test_rsvp'),
    path('send-reminders/', views.send_automatic_reminders, name='send_automatic_reminders'),
    path('bridesmaids/', BridesmaidListCreateView.as_view(), name='bridesmaid-list-create'),
    path('bridesmaids/<int:pk>/', BridesmaidDetailView.as_view(), name='bridesmaid-detail'),
    path('groomsmen/', GroomsmanListCreateView.as_view(), name='groomsman-list-create'),
    path('groomsmen/<int:pk>/', GroomsmanDetailView.as_view(), name='groomsman-detail'),
    path('event/<slug:slug>/', event_detail_page, name='event-detail-page'),
]
