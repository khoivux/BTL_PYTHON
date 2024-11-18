
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
from django.db.models import Q, Count, Case, When, IntegerField

from booking_manager.models import Booking
from homestay_manager.models import Homestay, HomestayFacilities
from django.http import JsonResponse
from .models import Booking
from django.utils import timezone
from datetime import datetime

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
    
    if not checkin_date_str or not checkout_date_str :
        context['error_message'] = 'Ngày nhận và trả phòng không được trống!'
        return render(request, 'product.html', context)
    checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date() 
    checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
    if checkin_date >= checkout_date or checkin_date < datetime.today().date():
        context['checkin_date'] = checkin_date
        context['checkout_date'] = checkout_date
        context['error_message'] = 'Ngày nhận và trả phòng không phù hợp!'
        return render(request, 'product.html', context)
    checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date() 
    checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
    print('create_booking')
    print(checkin_date)
    homestaytmp = Homestay.objects.filter(id=id).annotate(
        invalid_bookings=Count(
            Case(
                When(
                    ~(
                        Q(booking__checkin_date__gt=checkout_date) |  
                        Q(booking__checkout_date__lt=checkin_date) |   
                        Q(booking__isnull=True)
                    ),
                    then=1
                ),
                output_field=IntegerField()
            )
        )
    ).filter(invalid_bookings=0)
        
    
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

        context['checkin_date'] = checkin_date
        context['checkout_date'] = checkout_date

        context['stay_duration'] = stay_duration
        context['rent_price'] = rent_price
        context['province'] = homestay.province

        return render(request, 'booking.html', context)
    
def payment(request):
    if request.method == "POST":
        
        
        user_id = request.session.get('userId', None)
        print(user_id)
        homestay_id = request.POST.get('homestay_id')
        homestay_name = request.POST.get('homestay_name')
        homestay_address = request.POST.get('homestay_address')
        homestay_province = request.POST.get('homestay_province')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        stay_duration = request.POST.get('stay_duration')
        rent_price = request.POST.get('rent_price') + "000"
        services = request.POST.getlist('services')
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
        total =int(rent_price)
        checkin_date_time = str(datetime.strptime(checkin_date, '%b. %d, %Y').date())
        checkout_date_time = str(datetime.strptime(checkout_date, '%b. %d, %Y').date())
        for service in services:
            if(service == "Cầu hôn"):
                total += 2000000
            elif ( service == "Ăn uống"):
                total += 300000*int(stay_duration)
            elif ( service == "Thể thao"):
                total += 700000
            elif (service == "Đi lại"):
                total += 100000*int(stay_duration)
        data = {
                        "homestay_id" : homestay_id,
                        "homestay_name": homestay_name,
                        "homestay_address": homestay_address,
                        "homestay_province": homestay_province,
                        "checkin_date": checkin_date_time,
                        "checkout_date": checkout_date_time,
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
                        "onTime": onTime,
                        "total" : total,
                    }

    
        if user_id:
            
            print("userID")
            print(checkin_date_time)
            booking = Booking.objects.create(
                            booking_time=timezone.now(),  # Cập nhật thời gian hiện tại
                            checkin_date=checkin_date_time,
                            checkout_date=checkout_date_time,
                            status="Chưa thanh toán",  
                            homestay_id=1,
                            user_id=user_id,
                            bill_info=data
            )
            print(data)
            return render(request, 'hoadon.html', {'data': data})
        else:
            #yêu cầu đăng nhập
            return redirect ("/login")
            #hoặc vẫn sẽ cho thanh toán nhưng không lưu bills
