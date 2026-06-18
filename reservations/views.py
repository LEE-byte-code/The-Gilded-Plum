import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .forms import ReservationForm, ContactForm
from .models import Reservation, ChefsTableSlot, ContactInquiry
from menu.decorators import rate_limit
from menu.models import MenuItem


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def index(request):
    form = ReservationForm(initial={'date': timezone.localdate().isoformat()})
    contact_form = ContactForm()
    today = timezone.localdate()
    chef_slot, _ = ChefsTableSlot.objects.get_or_create(
        date=today,
        defaults={'available_seats': 6, 'total_seats': 6},
    )

    chef_data = {
        'available_seats': chef_slot.available_seats,
        'total_seats': chef_slot.total_seats,
    }

    return render(request, 'index.html', {
        'form': form,
        'contact_form': contact_form,
        'chef_data_json': json.dumps(chef_data),
        'chef_available': chef_slot.available_seats,
        'chef_total': chef_slot.total_seats,
        'confirmed': request.GET.get('confirmed'),
    })


@rate_limit('book_reservation', max_requests=10, window=60)
def book_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            if reservation.zone == 'chef':
                today = timezone.localdate()
                chef_slot, _ = ChefsTableSlot.objects.get_or_create(
                    date=today,
                    defaults={'available_seats': 6, 'total_seats': 6},
                )
                if chef_slot.available_seats > 0:
                    chef_slot.available_seats -= 1
                    chef_slot.save()

            send_mail(
                subject=f"Reservation Confirmed — The Gilded Plum",
                message=(
                    f"Dear {reservation.name},\n\n"
                    f"Your table has been confirmed.\n\n"
                    f"Date: {reservation.date}\n"
                    f"Time: {reservation.time}\n"
                    f"Guests: {reservation.guests}\n"
                    f"Zone: {reservation.get_zone_display()}\n\n"
                    f"We look forward to serving you.\n"
                    f"— The Gilded Plum"
                ),
                from_email=None,
                recipient_list=[reservation.email],
            )

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'reservation': {
                        'name': reservation.name,
                        'date': reservation.date.isoformat(),
                        'time': reservation.time,
                        'guests': reservation.guests,
                        'zone': reservation.get_zone_display(),
                    },
                })

            return redirect('/?confirmed=true')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                }, status=400)

            today = timezone.localdate()
            try:
                chef_slot, _ = ChefsTableSlot.objects.get_or_create(
                    date=today,
                    defaults={'available_seats': 6, 'total_seats': 6},
                )
                chef_data = {
                    'available_seats': chef_slot.available_seats,
                    'total_seats': chef_slot.total_seats,
                }
            except Exception:
                chef_data = {'available_seats': 6, 'total_seats': 6}

            return render(request, 'index.html', {
                'form': form,
                'errors': form.errors,
                'chef_data_json': json.dumps(chef_data),
                'chef_available': chef_data['available_seats'],
                'chef_total': chef_data['total_seats'],
            })

    return redirect('/')


@require_POST
@rate_limit('contact', max_requests=5, window=60)
def submit_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        inquiry = form.save()

        send_mail(
            subject=f"New Inquiry from {inquiry.name} — The Gilded Plum",
            message=(
                f"Name: {inquiry.name}\n"
                f"Email: {inquiry.email}\n"
                f"Phone: {inquiry.phone}\n"
                f"Preferred Contact: {inquiry.preferred_contact}\n\n"
                f"Message:\n{inquiry.message}"
            ),
            from_email=None,
            recipient_list=[settings.DEFAULT_FROM_EMAIL] if settings.DEFAULT_FROM_EMAIL else [],
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        messages.success(request, "Thank you! We'll be in touch soon.")
        return redirect('/#contact')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        messages.error(request, "Please correct the errors below.")
        return redirect('/#contact')


# ---------------------------------------------------------------------------
# Staff dashboard
# ---------------------------------------------------------------------------

@login_required
def dashboard(request):
    today = timezone.localdate()
    reservations_today = Reservation.objects.filter(date=today).order_by('time')
    reservations_upcoming = Reservation.objects.filter(date__gt=today, status__in=['pending', 'confirmed']).order_by('date', 'time')[:20]
    recent_inquiries = ContactInquiry.objects.filter(is_read=False)[:10]
    menu_items = MenuItem.objects.select_related('category').all()
    chef_slot, _ = ChefsTableSlot.objects.get_or_create(
        date=today,
        defaults={'available_seats': 6, 'total_seats': 6},
    )

    return render(request, 'dashboard.html', {
        'reservations_today': reservations_today,
        'reservations_upcoming': reservations_upcoming,
        'recent_inquiries': recent_inquiries,
        'menu_items': menu_items,
        'chef_slot': chef_slot,
        'today': today,
    })


@login_required
@require_POST
def dashboard_update_status(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    new_status = request.POST.get('status')
    if new_status in dict(Reservation.STATUS_CHOICES):
        reservation.status = new_status
        reservation.save()
    return redirect('dashboard')


@login_required
@require_POST
def dashboard_toggle_menu(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.is_available = not item.is_available
    item.save()
    return redirect('dashboard')
