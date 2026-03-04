from django.contrib import admin
from .models import Table, Category, MenuItem, Order, OrderItem
from django.utils.safestring import mark_safe


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'total_price', 'status', 'payment_confirmed', 'created_at')
    list_filter = ('status', 'payment_confirmed')
    inlines = [OrderItemInline]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'qr_preview')

    def qr_preview(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="80"/>')
        return "No QR"

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
admin.site.register(Category)