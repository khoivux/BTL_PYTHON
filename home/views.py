from gc import get_objects
from django.shortcuts import render
from .models import Homestay

def get_home(request):
    return render(request,'home.html')

def search_view(request):
    query = request.GET.get('location')
    ratings = request.GET.getlist('ratings')
    locations = request.GET.getlist('locations')
    prices = request.GET.getlist('prices')

    homestays = Homestay.objects.all()  # Lấy tất cả homestays

    # Nếu có tìm kiếm theo tên homestay
    if query:
        homestays = Homestay.objects.filter(province__name__icontains=query)
    if ratings:
        homestays = homestays.filter(rating__in=ratings)
    if prices:
        homestays = homestays.filter(price__in=prices)
    if locations:
        locations = [loc for loc in locations if loc]
        if locations:
            homestays = homestays.filter(province__id__in=locations)
    

    context = {
        'homestays': homestays,
        'selected_ratings': ratings,
        'selected_prices': prices,
        'selected_locations': locations,
    }
    return render(request, 'search.html', context)


def product_detail(request, id):
    homestay = Homestay.objects.filter(id=id).first()

    context = {
        'homestay': homestay,
    }
    return render(request, 'product.html', context)