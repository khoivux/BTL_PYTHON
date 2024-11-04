from gc import get_objects
from django.shortcuts import render
from homestay_manager.models import Homestay

def get_home(request):
    return render(request,'home.html')

def search_view(request):
    query = request.GET.get('location')
    ratings = request.GET.getlist('ratings')
    homefacilities = request.GET.getlist('homefacilities')
    prices = request.GET.getlist('prices')
    sort_option = request.GET.get('sort', 'asc')

    homestays = Homestay.objects.all()  # Lấy tất cả homestays

    # Nếu có tìm kiếm theo tên homestay
    if query:
        homestays = Homestay.objects.filter(province__name__icontains=query)
    if ratings:
        homestays = homestays.filter(rating__in=ratings)
    
    if homefacilities:
        homestays = homestays.filter(facilities__id__in=homefacilities).distinct()
       
    
     # Sắp xếp theo giá
    if sort_option == 'asc':
        homestays = homestays.order_by('price')
    elif sort_option == 'desc':
        homestays = homestays.order_by('-price')

    context = {
        'homestays': homestays,
        'selected_ratings': ratings,
        'selected_prices': prices,
        'selected_homefacilities': homefacilities,
        'current_sort': sort_option,
    }
    return render(request, 'search.html', context)


def product_detail(request, id):
    homestay = Homestay.objects.filter(id=id).first()

    context = {
        'homestay': homestay,
    }
    return render(request, 'product.html', context)