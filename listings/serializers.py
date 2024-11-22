# listings/serializers.py

from rest_framework import serializers
from .models import Listing, Booking, Review
from accounts.models import CustomUser
# Сериализатор для бронирования
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
# Сериализатор для объявления (listing)
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price', 'rooms',
            'property_type', 'status', 'created_at', 'updated_at', 'landlord'
        ]
# Сериализатор для отзыва (review)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'listing', 'tenant', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']
