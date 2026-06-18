from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    preferred_contact = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('either', 'Either'),
    ], default='email')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact inquiries'

    def __str__(self):
        return f"{self.name} — {self.created_at.date()}"


class Reservation(models.Model):
    ZONE_CHOICES = [
        ('hall', 'Grand Hall'),
        ('window', 'Window Seating'),
        ('booth', 'Saffron Booths'),
        ('bar', 'Sommelier Bar'),
        ('chef', "Chef's Table"),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.CharField(max_length=20)
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES, default='hall')
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.name} — {self.get_zone_display()} — {self.date} at {self.time}"


class ChefsTableSlot(models.Model):
    date = models.DateField(unique=True)
    total_seats = models.PositiveIntegerField(default=6)
    available_seats = models.PositiveIntegerField(default=6)
    price_per_guest = models.DecimalField(max_digits=6, decimal_places=2, default=180.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Chef's Table — {self.date} ({self.available_seats}/{self.total_seats} seats)"
