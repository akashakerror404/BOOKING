
from django.test import TestCase
from django.utils import timezone
from .models import FitnessClass, Booking
from rest_framework.test import APIClient
from rest_framework import status
import json

class FitnessClassAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.yoga_class = FitnessClass.objects.create(
            name='YOGA',
            date_time=timezone.now() + timezone.timedelta(days=1),
            instructor='John Doe',
            capacity=10,
            available_slots=10
        )
        self.valid_payload = {
            'fitness_class': self.yoga_class.id,
            'client_name': 'Test User',
            'client_email': 'test@example.com'
        }
        self.invalid_payload = {
            'fitness_class': self.yoga_class.id,
            'client_name': '',
            'client_email': 'invalid-email'
        }
    
    def test_get_all_classes(self):
        response = self.client.get('/api/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_valid_booking(self):
        response = self.client.post(
            '/api/book/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        
        # Verify slots decreased
        self.yoga_class.refresh_from_db()
        self.assertEqual(self.yoga_class.available_slots, 9)
    
    def test_create_invalid_booking(self):
        response = self.client.post(
            '/api/book/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_client_bookings(self):
        # Create a booking first
        Booking.objects.create(
            fitness_class=self.yoga_class,
            client_name='Test User',
            client_email='test@example.com'
        )
        
        response = self.client.get('/api/bookings/?email=test@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_client_bookings_no_email(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)