from django.urls import path
from .views import EventListCreateView, EventRetrieveUpdateDestroyView
from . import views

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<slug:slug>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<slug:event_slug>/rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('events/<slug:event_slug>/rsvp/export/', views.export_rsvp_csv, name='export_rsvp_csv'),
]
