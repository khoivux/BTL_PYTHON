from django.contrib import admin
from .models import Booking, BookingService
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
import openpyxl
from io import BytesIO

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_time', 'checkin_date', 'checkout_date', 'get_amount', 'status', 'homestay', 'user')
    actions = ['view_booking_and_revenue_charts', 'export_booking_data_to_excel']

    def view_booking_and_revenue_charts(self, request, queryset):
        booking_count_data = {f"{hour}:00": 0 for hour in range(24)}  
        bookings = Booking.objects.all()

        for booking in bookings:
            adjusted_booking_time = booking.booking_time
            booking_hour = adjusted_booking_time.hour
            booking_count_data[f"{booking_hour}:00"] += 1

        
        fig1, ax1 = plt.subplots(figsize=(10, 6)) 
        hours = ['0:00-1:00', '1:00-2:00', '2:00-3:00', '3:00-4:00', '4:00-5:00', '5:00-6:00', 
 '6:00-7:00', '7:00-8:00', '8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00', 
 '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', 
 '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-0:00']

        counts = list(booking_count_data.values())

        
        ax1.bar(hours, counts, color='skyblue')
        ax1.set_title('Số lượng đặt phòng theo giờ tạo (booking_time)')
        ax1.set_xlabel('Giờ')
        ax1.set_ylabel('Số lượng đặt phòng')
        ax1.tick_params(axis='x', rotation=45)

        # Lưu biểu đồ số lượng đặt phòng vào buffer
        buf1 = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        chart1 = base64.b64encode(buf1.read()).decode('utf-8')
        buf1.close()
        plt.close(fig1)  # Đảm bảo đóng biểu đồ sau khi lưu

        # Biểu đồ doanh thu theo tháng
        revenue_data = {f"{month}": 0 for month in range(1, 13)}  
        for booking in bookings:
            booking_month = booking.checkin_date.month  
            revenue_data[f"{booking_month}"] += int(booking.bill_info['total']) / 1e6

        months = list(revenue_data.keys())
        revenues = list(revenue_data.values())

        # Tạo biểu đồ doanh thu theo tháng
        fig2, ax2 = plt.subplots(figsize=(10, 6))  # Biểu đồ doanh thu theo tháng
        ax2.bar(months, revenues, color='lightgreen')
        ax2.set_title('Doanh thu theo tháng')
        ax2.set_xlabel('Tháng')
        ax2.set_ylabel('Doanh thu theo triệu VND')
        ax2.set_xticks(months)
        ax2.tick_params(axis='x', rotation=45)

        # Lưu biểu đồ doanh thu vào buffer
        buf2 = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        chart2 = base64.b64encode(buf2.read()).decode('utf-8')
        buf2.close()
        plt.close(fig2)  

        # HTML để hiển thị biểu đồ
        html = f"""
        <h1>Biểu Đồ Số Lượng Đặt Phòng Và Doanh Thu</h1>
        <h2>Số Lượng Đặt Phòng Theo Giờ Tạo</h2>
        <img src="data:image/png;base64,{chart1}" alt="Biểu Đồ Số Lượng Đặt Phòng">
        <h2>Doanh Thu Theo Tháng</h2>
        <img src="data:image/png;base64,{chart2}" alt="Biểu Đồ Doanh Thu">
        """
        return HttpResponse(html)

    def export_booking_data_to_excel(self, request, queryset):
        
        bookings = Booking.objects.all()
        
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Booking Data"

        
        ws.append(['ID', 'Checkin Date', 'Checkout Date', 'Amount', 'Status', 'Homestay', 'User'])

        
        for booking in bookings:
            
            user_value = booking.user.username if booking.user else 'N/A'

            ws.append([
                booking.id,
                booking.checkin_date,
                booking.checkout_date,
                int(booking.bill_info['total']),  
                booking.status,
                booking.homestay.name,  
                user_value,  
            ])

        
        excel_output = BytesIO()
        wb.save(excel_output)
        excel_output.seek(0)

        
        response = HttpResponse(excel_output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="booking_data.xlsx"'

        return response

    view_booking_and_revenue_charts.short_description = 'Xem Biểu Đồ Số Lượng Đặt Phòng và Doanh Thu'
    export_booking_data_to_excel.short_description = 'Xuất Dữ Liệu Đặt Phòng Ra Excel'

admin.site.register(BookingService)
