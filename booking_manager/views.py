from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q
from homestay_manager.models import Homestay, HomestayFacilities

# Create your views here.
def create_booking(request):
    id = request.GET.get('id')
    homestay = Homestay.objects.filter(id=id).first()
    checkout_date_str = request.GET.get('checkout_date')
    checkin_date_str = request.GET.get('checkin_date')
    facilities = homestay.facilities.all() 
    rooms = homestay.rooms.all()
    context = {
        'homestay': homestay,
        'facilities': facilities, 
        'rooms': rooms,
        }
    
    if not checkin_date_str or not checkout_date_str:
        context['error_message'] = 'Ngày nhận và trả phòng không được trống!'
        return render(request, 'product.html', context)

    checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date() 
    checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()

    homestaytmp = Homestay.objects.filter(id=id).filter(
                Q(booking__checkin_date__gt=checkout_date) |  
                Q(booking__checkout_date__lt=checkin_date) |   
                Q(booking__isnull=True)                         
            ).distinct()
    
    context['checkin_date'] = checkin_date
    context['checkout_date'] = checkout_date

    if not homestaytmp.exists():
        context['checkin_date'] = checkin_date
        context['checkout_date'] = checkout_date
        context['error_message'] = 'Homestay không sẵn có trong thời gian này!'
        return render(request, 'product.html', context)
    elif checkin_date >= checkout_date:
        context['checkin_date'] = checkin_date
        context['checkout_date'] = checkout_date
        context['error_message'] = 'Ngày nhận và trả phòng không phù hợp!'
        return render(request, 'product.html', context)
    else:
        stay_duration = (checkout_date - checkin_date).days
        rent_price = stay_duration * homestay.price
        
        context['stay_duration'] = stay_duration
        context['rent_price'] = rent_price
        context['province'] = homestay.province

        return render(request, 'booking.html', context)