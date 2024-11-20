from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from booking_manager.models import Booking
import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

@login_required
def getProfile(request):
    profile = request.user.profile  
    context = {
        'profile': profile 
    }
    return render(request, 'profile.html', context)
def edit(request):
    profile = request.user.profile  
    
    if request.method == 'POST':
        data = request.POST.copy()
        request.user.first_name = data.get('first_name', request.user.first_name)
        request.user.save()  
        form = ProfileForm(request.POST, instance=profile)  
        if form.is_valid():  
            form.save()  
            return redirect('profile')  
    else:
        form = ProfileForm(instance=profile) 

    context = {
        'form': form,  
        'profile': profile
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

def changePassword(request):
    return render(request, "changePassword.html")

def changePass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        print(current_password)
        if not user_id or not current_password or not new_password or not confirm_password:
            return JsonResponse({'success': False, 'message': 'Dữ liệu không hợp lệ.'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Mật khẩu mới không khớp.'})

        try:
            user = User.objects.get(id=user_id)

            if not user.check_password(current_password):
                return JsonResponse({'success': False, 'message': 'Mật khẩu hiện tại không đúng.'})

            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True, 'message': 'Mật khẩu đã được cập nhật thành công.'})

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Người dùng không tồn tại.'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ.'})