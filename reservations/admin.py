from django.contrib import admin
from .models import Reservation, ChefsTableSlot, ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'preferred_contact', 'is_read', 'created_at']
    list_filter = ['is_read', 'preferred_contact']
    search_fields = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    actions = ['mark_read', 'mark_unread']

    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = "Mark selected as Read"

    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_unread.short_description = "Mark selected as Unread"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'guests', 'zone', 'status', 'created_at']
    list_filter = ['status', 'zone', 'date']
    search_fields = ['name', 'email', 'phone']
    date_hierarchy = 'date'
    actions = ['mark_confirmed', 'mark_cancelled']

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = "Mark selected as Confirmed"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = "Mark selected as Cancelled"


@admin.register(ChefsTableSlot)
class ChefsTableSlotAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_seats', 'available_seats', 'price_per_guest']
    list_filter = ['date']
    date_hierarchy = 'date'
