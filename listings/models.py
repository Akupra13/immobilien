from django.db import models
from accounts.models import CustomUser
from datetime import timedelta
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    rooms = models.IntegerField()
    ad_type = models.CharField(max_length=50, choices=[('rent', 'Rent'), ('sale', 'Sale')])
    is_active = models.BooleanField(default=True)
    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    property_type = models.CharField(max_length=50, choices=[('apartment', 'Apartment'), ('house', 'House')], default='apartment')
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    updated_at = models.DateTimeField(auto_now=True)
    is_booked = models.BooleanField(default=False)  # Флаг забронировано
    booking_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Ожидает подтверждения'), ('approved', 'Подтверждено'), ('rejected', 'Отклонено')],
        default='pending'
    )
    def __str__(self):
        return self.title
    def is_available(self):
        """Проверка, доступно ли объявление для бронирования."""
        return self.is_active and self.status == 'active'
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def can_cancel(self):
        """Проверка, можно ли отменить бронирование (не позднее 7 дней до начала)."""
        return self.start_date > (self.created_at + timedelta(days=7))
    def confirm(self):
        """Подтвердить бронирование."""
        self.status = 'confirmed'
        self.save()
    def reject(self):
        """Отклонить бронирование."""
        self.status = 'rejected'
        self.save()
    def __str__(self):
        return f"{self.tenant.email} - {self.listing.title}"
class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()  # От 1 до 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review for {self.listing.title} by {self.tenant.email}"



