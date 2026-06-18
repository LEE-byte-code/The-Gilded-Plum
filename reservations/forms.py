from django import forms
from django.utils import timezone
from .models import Reservation, ContactInquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'message', 'preferred_contact']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your event, dietary needs, or any questions...'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'zone', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'id': 'res-date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'id': 'res-special', 'placeholder': 'Let us know about dietary restrictions, allergies, or special celebrations...'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError("Date cannot be in the past.")
        return date

    def clean_guests(self):
        guests = self.cleaned_data['guests']
        if guests > 20:
            raise forms.ValidationError("Maximum 20 guests per reservation.")
        return guests
