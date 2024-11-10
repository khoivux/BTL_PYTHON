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
    checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date() 
    checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()

    homestaytmp = Homestay.objects.filter(id=id).filter(
                Q(booking__checkin_date__gt=checkout_date) |  
                Q(booking__checkout_date__lt=checkin_date) |   
                Q(booking__isnull=True)                         
            ).distinct()

    # Kiểm tra ngày tại trang product
    if not homestaytmp.exists():
       # Không thỏa mãn thì ở lại product
        context1 = {
        'homestay': homestay,
        'facilities': facilities,
        'checkout_date': checkout_date,
        'checkin_date': checkin_date, 
        }
        return render(request, 'product.html', context1)
    else:
        # Thỏa mãn thì đến trang booking
        stay_duration = (checkout_date - checkin_date).days
        rent_price = stay_duration * homestay.price
        context2 = {
            'homestay': homestay,
            'checkout_date': checkout_date,
            'checkin_date': checkin_date,
            'province': homestay.province,
            'stay_duration': stay_duration,
            'rent_price': rent_price,
            'facilities': facilities,
        }
        return render(request, 'booking.html', context2)