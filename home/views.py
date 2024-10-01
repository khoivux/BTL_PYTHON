from django.shortcuts import render
from .models import Homestay
def get_home(request):
    return render(request,'home.html')

def search_view(request):
    query = request.GET.get('search')
    homestays = Homestay.objects.all()  # Lấy tất cả homestays

    # Nếu có tìm kiếm theo tên homestay
    if query:
        homestays = homestays.filter(name__icontains=query)

    # Lọc kết quả dựa trên giá tiền và vị trí
    # min_price = request.GET.get('min_price')
    # max_price = request.GET.get('max_price')
    # location = request.GET.get('location')

    # if min_price:
    #     homestays = homestays.filter(price__gte=min_price)
    # if max_price:
    #     homestays = homestays.filter(price__lte=max_price)
    # if location:
    #     homestays = homestays.filter(location__icontains=location)

    context = {
        'homestays': homestays,  # Truyền danh sách homestays vào template
    }
    return render(request, 'search.html', context)#Tạm thời trả về home.html

