from django.contrib import admin
from .models import Province, Service, Homestay, Room, HomestayFacilities, HomestayRoom, Transaction
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from django.utils.safestring import mark_safe
from datetime import datetime
import numpy as np
from django.urls import path
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


# Register models
admin.site.register(Province)

class FacilityInline(admin.TabularInline):
    model = Homestay.facilities.through

class ServiceInline(admin.TabularInline):
    model = Homestay.services.through

class HomestayRoomInline(admin.TabularInline):
    model = HomestayRoom
    extra = 1

@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    inlines = [FacilityInline, ServiceInline, HomestayRoomInline]
    exclude = ('facilities', 'services')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(HomestayFacilities)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('homestay', 'amount', 'date', 'time')
    list_filter = ('date', 'homestay')
    actions = ['view_charts_action']

    def view_charts_action(self, request, queryset):
        """
        Action hiển thị biểu đồ khi người dùng chọn các giao dịch
        """
        # Xử lý danh sách các giao dịch được chọn
        # Trong trường hợp này, chúng ta không thực hiện gì với các giao dịch,
        # mà chỉ đơn giản là redirect người dùng đến trang biểu đồ.
        return HttpResponseRedirect(reverse('admin:transaction_chart'))

    # Đặt tên hiển thị cho Action
    view_charts_action.short_description = 'Xem Biểu Đồ'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Chỉnh sửa hoặc thêm thông tin bổ sung nếu cần
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/', self.transaction_chart, name='transaction_chart'),
        ]
        return custom_urls + urls

    def transaction_chart(self, request):
        # Vẽ biểu đồ ở đây (giống như đã mô tả ở các bước trước)
        revenue_data = {'month': [], 'revenue': []}
        current_year = datetime.now().year
        for month in range(1, 13):
            revenue = Transaction.total_revenue_for_month(current_year, month)
            revenue_data['month'].append(f"Tháng {month}")
            revenue_data['revenue'].append(revenue)

        # Biểu đồ Doanh Thu Theo Tháng
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(revenue_data['month'], revenue_data['revenue'], color='skyblue')
        ax1.set_title('Doanh thu theo tháng')
        ax1.set_xlabel('Tháng')
        ax1.set_ylabel('Doanh thu')
        plt.xticks(rotation=45)

        buf1 = io.BytesIO()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        chart1 = base64.b64encode(buf1.read()).decode('utf-8')
        buf1.close()
        plt.close(fig1)

        # Biểu đồ Số Lượng Đặt Theo Giờ
        transactions = Transaction.objects.all()
        hour_data = {'hour': [], 'count': []}

        if transactions.exists():
            hours = [transaction.time.hour for transaction in transactions]
            counts = pd.Series(hours).value_counts().sort_index()

            hour_data['hour'] = counts.index.tolist()
            hour_data['count'] = counts.values.tolist()

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.bar(hour_data['hour'], hour_data['count'], color='orange', alpha=0.7)
            ax2.set_title('Số lượng đặt phòng theo giờ trong ngày')
            ax2.set_xlabel('Giờ')
            ax2.set_ylabel('Số lượng đặt')
            plt.xticks(range(0, 24))

            buf2 = io.BytesIO()
            plt.savefig(buf2, format='png')
            buf2.seek(0)
            chart2 = base64.b64encode(buf2.read()).decode('utf-8')
            buf2.close()
            plt.close(fig2)

            html = f"""
            <h1>Biểu đồ thống kê</h1>
            <h2>Doanh thu theo tháng</h2>
            <img src="data:image/png;base64,{chart1}" alt="Biểu đồ Doanh Thu Theo Tháng">
            <h2>Số lượng đặt phòng theo giờ</h2>
            <img src="data:image/png;base64,{chart2}" alt="Biểu đồ Số Lượng Đặt Theo Giờ">
            """
            return HttpResponse(html)