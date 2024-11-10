from asyncio.windows_events import NULL
from gc import get_objects
from django.shortcuts import render
from homestay_manager.models import Homestay, HomestayFacilities, Service, Room
from django.db.models import Q
from datetime import datetime
def get_home(request):
    homestays = Homestay.objects.all()

    context = {
        'homestays': homestays,
    }
    return render(request,'home.html', context)

def search_view(request):
    address = request.GET.get('address')
    ratings = request.GET.getlist('ratings')
    # Sức chứa
    capacity = request.GET.get('capacity')  
    # Giá thuê
    priceFrom = request.GET.get('pricefrom')
    priceTo = request.GET.get('priceto')
    # Ngày đặt 
    checkin_date_str = request.GET.get('checkin-date')
    checkout_date_str = request.GET.get('checkout-date')
    # Tiện nghi, dịch vụ
    selected_facilities = request.GET.getlist('facilities')
    selected_services = request.GET.getlist('services')
    selected_rooms = request.GET.getlist('rooms')
    sort_option = request.GET.get('sort', 'asc')

    facilities = HomestayFacilities.objects.all()
    services = Service.objects.all()
    homestays = Homestay.objects.all()  # Lấy tất cả homestays
    rooms = Room.objects.all()

    # Nếu có tìm kiếm theo tên homestay
    if address:
        homestays = Homestay.objects.filter(province__name__icontains=address)
        if not homestays:
            homestays = Homestay.objects.filter(address__icontains=address)

    if priceFrom:
        homestays = homestays.filter(price__gte=priceFrom)
    if priceTo:
        homestays = homestays.filter(price__lte=priceTo)
    if ratings:
        homestays = homestays.filter(rating__in=ratings)
    if capacity:
        homestays = homestays.filter(capacity__gte=capacity)
    if selected_facilities:
        homestays = homestays.filter(facilities__id__in=selected_facilities)
    if selected_services:
        homestays = homestays.filter(services__id__in=selected_services)
    if selected_rooms:
        homestays = homestays.filter(rooms__id__in=selected_rooms).distinct()



    if checkin_date_str and checkout_date_str:
        checkin_date = datetime.strptime(checkin_date_str, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout_date_str, "%Y-%m-%d").date()
        homestays = homestays.filter(
            Q(booking__checkin_date__gt=checkout_date) |   # Ngày in > ngày checkout của Booking
            Q(booking__checkout_date__lt=checkin_date) |   # Ngày out < ngày checkin của Booking
            Q(booking__isnull=True)                 
        ).distinct()
        print(checkin_date)

    if sort_option == 'asc':
        homestays = homestays.order_by('price')
    elif sort_option == 'desc':
        homestays = homestays.order_by('-price')

    context = {
        'services': services,
        'capacity': capacity,
        'pricefrom' : priceFrom,
        'priceto' : priceTo,
        'address': address,
        'facilities' : facilities,
        'homestays': homestays,
        'rooms': rooms,
        'selected_ratings': ratings,
        'selected_facilities': selected_facilities,
        'selected_services': selected_services,
        'selected_rooms': selected_rooms,
        'current_sort': sort_option,
        'checkin_date': checkin_date_str,
        'checkout_date': checkout_date_str,
    }
    return render(request, 'search.html', context)

def product_detail(request, id):
    homestay = Homestay.objects.filter(id=id).first()
    facilities = homestay.facilities.all()    
    checkout_date = request.GET.get('checkout_date')
    checkin_date = request.GET.get('checkin_date')
    context = {
        'homestay': homestay,
        'facilities': facilities,
        'checkout_date': checkout_date,
        'checkin_date': checkin_date, 
    }
    return render(request, 'product.html', context)
