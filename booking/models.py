from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import pytz
import logging
logger = logging.getLogger(__name__)

class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
    ]
    
    name = models.CharField(max_length=50, choices=CLASS_TYPES)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.get_name_display()} with {self.instructor} at {self.date_time}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_slots = self.capacity
        super().save(*args, **kwargs)
    
    def is_available(self):
        return self.available_slots > 0 and self.date_time > timezone.now()
    
    def convert_timezone(self, timezone_str):
        try:
            new_tz = pytz.timezone(timezone_str)
            localized = pytz.timezone('Asia/Kolkata').localize(self.date_time)
            return localized.astimezone(new_tz)
        except Exception as e:
            logger.error(f"Timezone conversion error: {e}")
            return self.date_time

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class}"