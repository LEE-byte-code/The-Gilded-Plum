import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Reservation, ChefsTableSlot


class ReservationModelTest(TestCase):
    def test_default_status_is_pending(self):
        r = Reservation.objects.create(
            name='Test', email='a@b.com', phone='555',
            date='2026-12-25', time='7:00 PM', guests=2,
        )
        self.assertEqual(r.status, 'pending')

    def test_chefs_table_slot_default_seats(self):
        slot = ChefsTableSlot.objects.create(date='2026-12-25')
        self.assertEqual(slot.total_seats, 6)
        self.assertEqual(slot.available_seats, 6)
        self.assertEqual(float(slot.price_per_guest), 180.00)


class ReservationViewsTest(TestCase):
    def test_index_returns_200(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_book_reservation_get_redirects(self):
        resp = self.client.get(reverse('book'))
        self.assertEqual(resp.status_code, 302)

    def test_book_reservation_success(self):
        data = {
            'name': 'Alex Mercer',
            'email': 'alex@example.com',
            'phone': '555-0000',
            'date': timezone.localdate().isoformat(),
            'time': '7:00 PM',
            'guests': 2,
            'zone': 'hall',
        }
        resp = self.client.post(reverse('book'), data)
        self.assertEqual(resp.status_code, 302)  # Redirect on success
        self.assertEqual(Reservation.objects.count(), 1)

    def test_book_reservation_ajax_success(self):
        data = {
            'name': 'Alex Mercer',
            'email': 'alex@example.com',
            'phone': '555-0000',
            'date': timezone.localdate().isoformat(),
            'time': '7:00 PM',
            'guests': 2,
            'zone': 'hall',
        }
        resp = self.client.post(
            reverse('book'), data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertTrue(body['success'])
        self.assertEqual(body['reservation']['name'], 'Alex Mercer')

    def test_book_reservation_ajax_error(self):
        resp = self.client.post(
            reverse('book'), {'name': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 400)
        body = resp.json()
        self.assertFalse(body['success'])
        self.assertIn('errors', body)

    def test_chefs_table_decrements_on_booking(self):
        today = timezone.localdate()
        ChefsTableSlot.objects.create(date=today, available_seats=6, total_seats=6)

        data = {
            'name': 'Chef Guest',
            'email': 'chef@example.com',
            'phone': '555-1111',
            'date': today.isoformat(),
            'time': '8:00 PM',
            'guests': 2,
            'zone': 'chef',
        }
        self.client.post(reverse('book'), data)

        slot = ChefsTableSlot.objects.get(date=today)
        self.assertEqual(slot.available_seats, 5)

    def test_booking_invalid_date(self):
        data = {
            'name': 'Test',
            'email': 'a@b.com',
            'phone': '555',
            'date': '2020-01-01',
            'time': '7:00 PM',
            'guests': 2,
        }
        resp = self.client.post(reverse('book'), data)
        self.assertEqual(resp.status_code, 200)  # Re-renders with errors
        self.assertContains(resp, 'error')
        self.assertEqual(Reservation.objects.count(), 0)
