from django.shortcuts import render, get_object_or_404
from .models import Table, Category, MenuItem
from django.contrib.auth.decorators import login_required

def menu_view(request, table_number):
    table = get_object_or_404(Table, number=table_number)
    categories = Category.objects.all()
    items = MenuItem.objects.filter(available=True)

    context = {
        "table": table,
        "categories": categories,
        "items": items,
    }

    return render(request, "core/menu.html", context)

from django.http import JsonResponse
import json
from .models import Order, OrderItem, MenuItem


def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)

        table_number = data.get("table")
        items = data.get("items")

        table = Table.objects.get(number=table_number)

        total_price = 0
        order = Order.objects.create(table=table, total_price=0)

        for item in items:
            menu_item = MenuItem.objects.get(id=item["id"])
            quantity = item["quantity"]

            OrderItem.objects.create(
                order=order,
                item=menu_item,
                quantity=quantity
            )

            total_price += menu_item.price * quantity

        order.total_price = total_price
        order.save()

        return JsonResponse({
            "status": "success",
            "order_id": order.id,
            "redirect_url": f"/order/{order.id}/"
        })

    return JsonResponse({"status": "error"})

def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "core/order_status.html", {"order": order})

@login_required
def kitchen_dashboard(request):
    orders = Order.objects.filter(
        status__in=['confirmed', 'preparing']
    ).order_by('-created_at')
    return render(request, "core/kitchen.html", {"orders": orders})

from django.shortcuts import redirect

@login_required
def update_status(request, order_id, new_status):
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
    return redirect('kitchen_dashboard')

from django.http import JsonResponse

def kitchen_data(request):
    orders = Order.objects.filter(
        status__in=['confirmed', 'preparing']
    ).values('id')

    return JsonResponse({
        "orders": list(orders)
    })

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("kitchen_dashboard")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")