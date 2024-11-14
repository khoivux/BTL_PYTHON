from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
@login_required
def getProfile(request):
    profile = request.user.profile  # Lấy thông tin profile của người dùng
    context = {
        'profile': profile  # Truyền dữ liệu profile vào context
    }
    return render(request, 'profile.html', context)
def edit(request):
    profile = request.user.profile  # Lấy thông tin profile của người dùng
    
    if request.method == 'POST':
        data = request.POST.copy()
        request.user.first_name = data.get('first_name', request.user.first_name)
        request.user.save()  # Lưu thông tin user
        form = ProfileForm(request.POST, instance=profile)  # Tạo form với dữ liệu từ request
        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            form.save()  # Lưu thông tin vào database
            return redirect('profile')  # Chuyển hướng đến trang profile sau khi lưu thành công
    else:
        form = ProfileForm(instance=profile)  # Nếu không phải POST, khởi tạo form với dữ liệu hiện tại

    context = {
        'form': form,  # Truyền form vào context
        'profile': profile  # Truyền dữ liệu profile vào context
    }
    return render(request, 'profile.html', context)