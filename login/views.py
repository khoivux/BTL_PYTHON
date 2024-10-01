from django.shortcuts import render
from django.shortcuts import redirect

def login(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        username = request.POST.get('username')  # Lấy giá trị của input name="username"
        password = request.POST.get('password')  # Lấy giá trị của input name="password"
        print(username)
        print(password)
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def inf(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form đăng ký
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

        # Nếu có lỗi, trả về form với thông báo lỗi
        if errors:
            return render(request, 'register.html', {'errors': errors})
        
        # Thêm logic để kiểm tra và lưu thông tin đăng ký vào database tại đây
        # Ví dụ, bạn có thể kiểm tra username đã tồn tại chưa, mật khẩu có đủ độ dài không, v.v.
        
        # Giả sử bạn muốn tạo một người dùng mới (nếu sử dụng mô hình User mặc định của Django):
        # from django.contrib.auth.models import User
        # if User.objects.filter(username=username).exists():
        #     return HttpResponse("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")
        # else:
        #     user = User.objects.create_user(username=username, password=password, email=email)
        #     user.save()
        #     return HttpResponse("Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
        print(username)
        print(password)
        print(email)
        return redirect('login')
    return render(request, 'register.html')  # Đảm bảo trả về một đối tượng HttpRespons