from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from booking_manager.models import Booking
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
        
        # Thỏa mãn thì đến trang booking
        stay_duration = (checkout_date - checkin_date).days
        rent_price = stay_duration * homestay.price
        
        context['stay_duration'] = stay_duration
        context['rent_price'] = rent_price
        context['province'] = homestay.province

        return render(request, 'booking.html', context)
    
def payment(request):
    if request.method == "POST":
        
        user_id = request.session.get('user_id', None)
        homestay_name = request.POST.get('homestay_name')
        homestay_address = request.POST.get('homestay_address')
        homestay_province = request.POST.get('homestay_province')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        stay_duration = request.POST.get('stay_duration')
        rent_price = request.POST.get('rent_price')
        services = request.POST.get('services')
        facilities = request.POST.get('facilities')
        lastName = request.POST.get('lastName') #lấy thông tin người đặt
        firstName = request.POST.get('firstName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        lastNameR = request.POST.get('lastNameR') #lấy thông tin người nhận
        firstNameR = request.POST.get('firstNameR')
        emailR =request.POST.get('emailR')
        phoneR = request.POST.get('phoneR')
        onTime = request.POST.get('onTime')
        
        data = {
                        "homestay_name": homestay_name,
                        "homestay_address": homestay_address,
                        "homestay_province": homestay_province,
                        "checkin_date": checkin_date,
                        "checkout_date": checkout_date,
                        "stay_duration": stay_duration,
                        "rent_price": rent_price,
                        "services": services,
                        "facilities": facilities,
                        "lastName": lastName,
                        "firstName": firstName,
                        "email": email,
                        "phone": phone,
                        "lastNameR": lastNameR,
                        "firstNameR": firstNameR,
                        "emailR": emailR,
                        "phoneR": phoneR,
                        "onTime": onTime
                    }

    
        if user_id:
            # Tạo một instance mới của Booking và lưu dữ liệu JSON vào trường booking_data
            booking = Booking.objects.create(
                            booking_time=timezone.now(),  # Cập nhật thời gian hiện tại
                            checkin_date=checkin_date,
                            checkout_date=checkout_date,
                            status="Chưa thanh toán",  # Ví dụ, trạng thái là 'Pending'
                            homestay_id=1,  # Giả sử homestay_id đã được chọn từ dữ liệu của bạn
                            user_id=user_id,  # Giả sử user_id là 1
                            booking_data=data  # Lưu dữ liệu JSON vào trường booking_data
            )
            return JsonResponse({"message": "Booking created successfully!"}) # sẽ thay thành chuyển đến trang thanh toán
        else:
            #yêu cầu đăng nhập
            return redirect ("/login")
            #hoặc vẫn sẽ cho thanh toán nhưng không lưu bills

