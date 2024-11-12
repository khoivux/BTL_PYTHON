from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .mail import send_email
from django.http import HttpResponse
import smtplib
from django.contrib import messages
import random
import string
def loginv(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        username = request.POST.get('username')  # Lấy giá trị của input name="username"
        password = request.POST.get('password')  # Lấy giá trị của input name="password"
        print(username)
        print(password)
        errors ={}
        if not username:
            errors['username'] = 'Vui lòng nhập tên đăng nhập'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if errors:
            return render(request, 'login.html', {'errors': errors})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['isLoggedIn'] = True  # Thêm trạng thái đăng nhập vào session
            request.session['userName'] = user.username  # Lưu tên người dùng
            return redirect('home')  # Chuyển hướng đến trang home
        else:
            errors['credentials'] = 'Tên đăng nhập hoặc mật khẩu không đúng'
            return render(request, 'login.html', {'errors': errors})
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def inf(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Lấy giá trị của input name="username"
        password = request.POST.get('password')  # Lấy giá trị của input name="password"
        email = request.POST.get('email')  # Lấy giá trị của input name="email"
        errors = {}
        if not username:
            errors['username'] = 'Vui lòng nhập tên đăng nhập'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if not email:
            errors['email'] = 'Vui lòng nhập email'

        if errors:
            return render(request, 'register.html', {'errors': errors})
        try:
            # Tạo người dùng mới
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()  # Lưu người dùng vào cơ sở dữ liệu
            
            print(username)
            print(password)
            print(email)

            # Chuyển hướng người dùng tới trang đăng nhập
            return redirect('login')
        
        except Exception as e:
            
            errors['username'] = 'Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác!'
            return render(request, 'register.html', {'errors': errors})
        
        
    return render(request, 'register.html') 

def forget(request):
    return render(request, 'forget.html')

def mail(request):
    print('mail duoc an!')
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Gửi mã OTP qua email
            otp = generate_otp()
            subject = "OTP reset password"
            body = f"Your verifications Code: {otp}"
            
            try:
                send_email(subject, body, email)
                messages.success(request, "Mã OTP đã được gửi tới email của bạn.")
                request.session['otp'] = otp
                print(otp)
                return render(request, 'forget.html', {'otp_sent': True,'otp':otp})
            except Exception as e:
                 messages.error(request, f"Đã có lỗi xảy ra khi gửi email: {e}")
            
            return render(request, 'forget.html')
        else:
            messages.error(request, "Vui lòng nhập email hợp lệ.")
            return render(request, 'forget.html')
    
    return render(request, 'forget.html')
    


def generate_otp():
    
    characters = string.ascii_letters + string.digits
    otp = ''.join(random.choices(characters, k=6))
    return otp

    