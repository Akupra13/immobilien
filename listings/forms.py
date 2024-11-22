# listings/forms
from django import forms
from .models import Listing,Booking
from django import forms
from .models import Listing
from datetime import date
class BookingForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today)
    end_date = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today)
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title',
                  'description',
                  'location',
                  'price',
                  'rooms',
                  'property_type',
                  'status',
                  ]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']