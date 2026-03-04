from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import json

from .models import Table, Category, MenuItem, Order, OrderItem


# ==========================
# CUSTOMER MENU
# ==========================

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


# ==========================
# CREATE ORDER
# ==========================

def create_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        table_number = data.get("table")
        items = data.get("items")

        table = get_object_or_404(Table, number=table_number)

        order = Order.objects.create(
            table=table,
            total_price=0
        )

        total_price = 0

        for item in items:

            menu_item = get_object_or_404(MenuItem, id=item["id"])
            quantity = int(item["quantity"])

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


# ==========================
# CUSTOMER ORDER STATUS
# ==========================

def order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(request, "core/order_status.html", {
        "order": order
    })


# ==========================
# KITCHEN DASHBOARD
# ==========================

@login_required
def kitchen_dashboard(request):

    orders = Order.objects.filter(
        status__in=["confirmed", "preparing"]
    ).order_by("created_at")  # priority sorting

    return render(request, "core/kitchen.html", {
        "orders": orders
    })


# ==========================
# UPDATE ORDER STATUS
# ==========================

@login_required
def update_status(request, order_id, new_status):

    order = get_object_or_404(Order, id=order_id)

    order.status = new_status

    if new_status == "cancelled":
        order.kitchen_message = "Kitchen cannot prepare this order. Please reorder."

    order.save()

    return redirect("kitchen_dashboard")


# ==========================
# LIVE ORDER CHECK (KITCHEN)
# ==========================

def kitchen_data(request):

    orders = Order.objects.filter(
        status__in=["confirmed", "preparing"]
    ).values("id")

    return JsonResponse({
        "orders": list(orders)
    })


# ==========================
# KITCHEN MESSAGE
# ==========================

@login_required
def send_kitchen_message(request, order_id):

    if request.method == "POST":

        order = get_object_or_404(Order, id=order_id)

        message = request.POST.get("message")

        order.kitchen_message = message
        order.save()

    return redirect("kitchen_dashboard")


# ==========================
# LOGIN
# ==========================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("kitchen_dashboard")

    return render(request, "core/login.html")


# ==========================
# LOGOUT
# ==========================

def logout_view(request):

    logout(request)

    return redirect("login")