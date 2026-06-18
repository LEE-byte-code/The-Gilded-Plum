import json
from datetime import date as date_type
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.validators import ValidationError
from reservations.models import Reservation, ChefsTableSlot
from .models import MenuItem, GalleryImage
from .decorators import rate_limit

VALID_ZONES = {'hall', 'window', 'booth', 'bar', 'chef'}
VALID_TIMES = {
    '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM',
    '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM',
    '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM',
}


def _serialize_menu_item(item):
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': float(item.price),
        'image': item.image,
        'category': item.category.name,
        'category_slug': item.category.slug,
        'ingredients': item.ingredients,
        'nutrition': {
            'cal': item.calories,
            'protein': item.protein,
            'carbs': item.carbs,
            'fat': item.fat,
        },
        'allergens': item.allergen_list(),
        'chefsNote': item.chefs_note,
        'pairing': item.wine_pairing,
        'tags': item.tag_list(),
        'isAvailable': item.is_available,
    }


@require_GET
def menu_list(request):
    items = MenuItem.objects.filter(is_available=True).select_related('category')
    data = [_serialize_menu_item(item) for item in items]
    return JsonResponse({'data': data})


@require_GET
def gallery_list(request):
    images = GalleryImage.objects.filter(is_active=True)
    data = [
        {
            'id': img.id,
            'src': img.image,
            'caption': img.caption,
            'alt': img.alt_text or img.caption,
        }
        for img in images
    ]
    return JsonResponse({'data': data})


@require_GET
def chef_table_availability(request):
    today = timezone.localdate()
    slot, _ = ChefsTableSlot.objects.get_or_create(
        date=today,
        defaults={'available_seats': 6, 'total_seats': 6},
    )
    return JsonResponse({
        'availableSeats': slot.available_seats,
        'totalSeats': slot.total_seats,
        'pricePerGuest': float(slot.price_per_guest),
    })


@require_GET
def time_slots(request):
    date_str = request.GET.get('date')
    zone = request.GET.get('zone', 'hall')

    if not date_str:
        return JsonResponse({'error': 'Date is required'}, status=400)

    if zone not in VALID_ZONES:
        return JsonResponse({'error': 'Invalid zone'}, status=400)

    try:
        parsed_date = date_type.fromisoformat(date_str)
        if parsed_date < timezone.localdate():
            return JsonResponse({'error': 'Date cannot be in the past'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format (use YYYY-MM-DD)'}, status=400)

    booked = Reservation.objects.filter(
        date=date_str,
        zone=zone,
        status__in=['pending', 'confirmed'],
    ).values_list('time', flat=True)

    available = [t for t in sorted(VALID_TIMES) if t not in booked]

    if zone == 'chef':
        try:
            slot = ChefsTableSlot.objects.get(date=date_str)
            return JsonResponse({
                'times': available,
                'availableSeats': slot.available_seats,
                'totalSeats': slot.total_seats,
            })
        except ChefsTableSlot.DoesNotExist:
            return JsonResponse({
                'times': available,
                'availableSeats': 6,
                'totalSeats': 6,
            })

    return JsonResponse({'times': available})


@csrf_exempt
@rate_limit('check_availability', max_requests=30, window=60)
def check_availability(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    date = body.get('date')
    time = body.get('time')
    zone = body.get('zone', 'hall')
    guests_raw = body.get('guests', 1)

    if not date or not time:
        return JsonResponse({'error': 'Date and time are required'}, status=400)

    if zone not in VALID_ZONES:
        return JsonResponse({'error': 'Invalid zone'}, status=400)

    if time not in VALID_TIMES:
        return JsonResponse({'error': 'Invalid time slot'}, status=400)

    try:
        parsed_date = date_type.fromisoformat(date)
        if parsed_date < timezone.localdate():
            return JsonResponse({'error': 'Date cannot be in the past'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format (use YYYY-MM-DD)'}, status=400)

    try:
        guests = int(guests_raw)
        if guests < 1 or guests > 20:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Guests must be a number between 1 and 20'}, status=400)

    existing = Reservation.objects.filter(
        date=date,
        time=time,
        zone=zone,
        status__in=['pending', 'confirmed'],
    ).count()

    max_per_slot = 1 if zone == 'chef' else 5

    return JsonResponse({
        'available': existing < max_per_slot,
        'existingBookings': existing,
        'maxCapacity': max_per_slot,
    })
