from asyncio.windows_events import NULL
from gc import get_objects
from django.shortcuts import render
from homestay_manager.models import Homestay, HomestayFacilities, Service, Room, HomestayRoom
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
        for facility_id in selected_facilities:
            homestays = homestays.filter(facilities__id=facility_id)
    if selected_services:
        for service_id in selected_services:
            homestays = homestays.filter(services__id=service_id)
    if selected_rooms:
        for room_id in selected_rooms:
            homestays = homestays.filter(rooms__id=room_id)

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
    
    if (not checkin_date_str) != (not checkout_date_str):
            context['error_message'] = 'Ngày nhận và trả phòng không được trống!'
            return render(request, 'search.html', context)

    if checkin_date_str and checkout_date_str:
        checkin_date = datetime.strptime(checkin_date_str, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout_date_str, "%Y-%m-%d").date()

        if checkin_date >= checkout_date or checkin_date < datetime.today().date():
            context['error_message'] = 'Ngày nhận và trả phòng không hợp lệ!'
            return render(request, 'search.html', context)
        
        
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

    context['homestays'] = homestays
    return render(request, 'search.html', context)

def product_detail(request, id):
    homestay = Homestay.objects.filter(id=id).first()
    facilities = homestay.facilities.all() 
    homestay_rooms = HomestayRoom.objects.filter(homestay=homestay)
    rooms = homestay.rooms.all()
    checkout_date = request.GET.get('checkout_date')
    checkin_date = request.GET.get('checkin_date')
    #checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d").date()
    #checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()
    print('detail:')
    print(checkin_date)
    context = {
        'homestay': homestay,
        'facilities': facilities,
        'checkout_date': checkout_date,
        'checkin_date': checkin_date, 
        'homestay_rooms': homestay_rooms,
        'rooms': rooms,
    }
    return render(request, 'product.html', context)
