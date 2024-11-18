from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from booking_manager.models import Booking
import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

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

def user_invoices(request):
    user_id = request.session.get("userId")
    user = User.objects.get(id=user_id)
    
    invoices = Booking.objects.filter(user=user)
    invoices_data = []
    for invoice in invoices:
        print(invoice.bill_info)
        invoice_data = {
            'id': invoice.id,
            'checkinDate': invoice.checkin_date.strftime('%Y-%m-%d'),  # Chuyển đổi thành chuỗi
            'checkoutDate': invoice.checkout_date.strftime('%Y-%m-%d'),
            'amount': invoice.bill_info['total'],
            'status': invoice.status,
            'bill_info': invoice.bill_info,
            'homestayName' : invoice.bill_info['homestay_name'],
        }
        invoices_data.append(invoice_data)
    data = {
        'userInfo': {
            'id': user.id,
            'name': user.first_name + user.last_name,
            'email': user.email,
        },
        
        
        'invoices': invoices_data
    }
    return render(request, 'test.html', {'data': json.dumps(data)})
def delete(request):
    if request.method == 'POST':
        # Lấy ID từ request.POST thay vì từ request.body
        booking_id = request.POST.get('id')

        if booking_id:
            try:
                # Tìm và xóa giao dịch với ID này
                booking = get_object_or_404(Booking, id=booking_id)
                booking.delete()
                messages.success(request, f"Giao dịch ID: {booking_id} đã được xóa thành công!")
                return redirect('/profile/invoices/')  # Redirect về trang profile sau khi xóa thành công
            except Booking.DoesNotExist:
                messages.error(request, "Giao dịch không tồn tại.")
        else:
            messages.error(request, "Không có ID giao dịch.")
        
    return redirect('/profile/invoices/')