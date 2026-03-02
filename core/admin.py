from django.contrib import admin
from .models import Table, Category, MenuItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'total_price', 'status', 'payment_confirmed', 'created_at')
    list_filter = ('status', 'payment_confirmed')
    inlines = [OrderItemInline]


admin.site.register(Table)
admin.site.register(Category)
admin.site.register(MenuItem)