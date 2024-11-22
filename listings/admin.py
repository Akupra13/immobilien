# listings/admin.py
from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id',
                  'title',
                  'description',
                  'location',
                  'price',
                  'rooms',
                  'property_type',
                  'status',
                  'created_at',
                  'updated_at',
                  )

    search_fields = ['title', 'description']



