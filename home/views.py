from django.shortcuts import render
from .models import Homestay
from .forms import HomestayFilterForm

def get_home(request):
    return render(request,'home1.html')

def search_view(request):
    query = request.GET.get('name')
    homestays = Homestay.objects.all()  # Lấy tất cả homestays

    # Nếu có tìm kiếm theo tên homestay
    if query:
        homestays = homestays.filter(name__icontains=query)

    ratings = request.GET.getlist('ratings')
    prices = request.GET.getlist('prices')
    locations = request.GET.getlist('locations')

    if ratings:
        homestays = homestays.filter(rating__in=ratings)
    if prices:
        homestays = homestays.filter(price__in=prices)
    if locations:
        homestays = Homestay.objects.filter(province__id__in=locations)

    context = {
        'homestays': homestays,  # Truyền danh sách homestays vào template
    }
    return render(request, 'search.html')#Tạm thời trả về home.html

# def search_view(request, name):
#     form = HomestayFilterForm(request.GET or None)  # Khởi tạo form lọc
#     homestays = Homestay.objects.filter(name__icontains=name)  # Tìm homestay theo tên

#     # Lọc kết quả theo các filter
#     if form.is_valid():
#         min_price = form.cleaned_data.get('min_price')
#         max_price = form.cleaned_data.get('max_price')

#         if min_price is not None:  # Kiểm tra nếu có giá tối thiểu
#             queryset = queryset.filter(price__gte=min_price)  # Lọc theo giá lớn hơn hoặc bằng
#         if max_price is not None:  # Kiểm tra nếu có giá tối đa
#             queryset = queryset.filter(price__lte=max_price)  # Lọc theo giá nhỏ hơn hoặc bằng


#     return render(request, 'search_results.html', {
#         'form': form, 
#         'homestays': homestays,  # Truyền danh sách homestay tìm được
#         'search': name  # Truyền tên đã tìm kiếm
#     })