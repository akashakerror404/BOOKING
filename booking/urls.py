from django.urls import path
from .views import FitnessClassListView, CreateBookingView, ClientBookingsView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='classes-list'),
    path('book/', CreateBookingView.as_view(), name='create-booking'),
    path('bookings/', ClientBookingsView.as_view(), name='client-bookings'),
]