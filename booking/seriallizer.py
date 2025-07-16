# bookings/serializers.py
from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone

class FitnessClassSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'available_slots', 'is_available']
        read_only_fields = ['available_slots', 'is_available']
    
    def get_is_available(self, obj):
        return obj.is_available()

class BookingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fitness_class.name', read_only=True)
    class_time = serializers.DateTimeField(source='fitness_class.date_time', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'class_name', 'class_time', 'client_name', 'client_email', 'booking_date']
        read_only_fields = ['booking_date']
    
    def validate_fitness_class(self, value):
        if not value.is_available():
            raise serializers.ValidationError("This class is no longer available for booking.")
        return value