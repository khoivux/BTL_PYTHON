from asyncio.windows_events import NULL
from gc import get_objects
from django.shortcuts import render
from homestay_manager.models import Homestay, HomestayFacilities, Service

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
    checkin_date = request.GET.get('checkin-date')
    checkout_date = request.GET.get('checkout-date')
    # Tiện nghi, dịch vụ
    homefacilities = request.GET.getlist('homefacilities')
    homeservices = request.GET.get('homeservices')

    sort_option = request.GET.get('sort', 'asc')

    facilities = HomestayFacilities.objects.all()
    services = Service.objects.all()
    homestays = Homestay.objects.all()  # Lấy tất cả homestays

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
    if homefacilities:
        homestays = homestays.filter(facilities__id__in=homefacilities).distinct()
    # if homeservices:
    #     homestays = homestays.filter(services__id__in=homeservices).distinct()

     # Sắp xếp theo giá
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
        'selected_ratings': ratings,
        'selected_facilities': homefacilities,
       # 'selected_services': homeservices,
        'current_sort': sort_option,
    }
    return render(request, 'search.html', context)

def product_detail(request, id):
    homestay = Homestay.objects.filter(id=id).first()

    context = {
        'homestay': homestay,
    }
    return render(request, 'product.html', context)
