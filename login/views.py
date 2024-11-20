from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .mail import send_email
from django.http import HttpResponse
from django.http import JsonResponse
import smtplib
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import random
import string

def custom_logout(request):
    
    logout(request)              
    request.session.flush()
    return JsonResponse({'message': 'Đăng xuất thành công'}, status=200)
def loginv(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        username = request.POST.get('username')
        password = request.POST.get('password')
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
            request.session['isLoggedIn'] = True  
            request.session['first_name'] = user.first_name 
            request.session['userId'] = user.id 
            print(request.session.get('userId'))
            return redirect('home')
        else:
            errors['credentials'] = 'Tên đăng nhập hoặc mật khẩu không đúng'
            return render(request, 'login.html', {'errors': errors})
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def inf(request):
    if request.method == "POST":
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        email = request.POST.get('email') 
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
            user.save()  
            
            print(username)
            print(password)
            print(email)

            
            return redirect('login')
        
        except Exception as e:
            
            if 'username' in str(e):
                errors['username'] = 'Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác!'
            elif 'email' in str(e):
                errors['email'] = 'Email đã tồn tại, vui lòng chọn email khác!'
            return render(request, 'register.html', {'errors': errors})
        
        
    return render(request, 'register.html') 

def forget(request):
    return render(request, 'forget.html')

def mail(request):
    print('mail duoc an!')
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)  # Tìm người dùng theo email
        except User.DoesNotExist:
            user = None
        
        if user:
            print("có")
            # Gửi mã OTP qua email
            otp = generate_otp()
            subject = "OTP reset password"
            body = f"Your verifications Code: {otp}"
            
            try:
                send_email(subject, body, email)
                request.session['otp'] = otp
                print(otp)
                return render(request, 'forget.html', {'otp_sent': True,'otp':otp,'id': user.id})
            except Exception as e:
                return render(request, 'forget.html', {'errors': "không gửi được mail"})
                
        else:
            print("không")
            return render(request, 'forget.html', {'errors': "Email không tồn tại!"})

    


def generate_otp():
    
    characters = string.ascii_letters + string.digits
    otp = ''.join(random.choices(characters, k=6))
    return otp



def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Lấy dữ liệu JSON từ request
            user_id = data.get('user_id')
            new_password = data.get('new_password')
            print(user_id)
            # Kiểm tra và xử lý user_id và new_password
            if not user_id or not new_password:
                return JsonResponse({'success': False, 'message': 'Dữ liệu không hợp lệ.'})

            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': True, 'message': 'Mật khẩu đã được cập nhật thành công.'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Người dùng không tồn tại.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Dữ liệu JSON không hợp lệ.'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ.'})