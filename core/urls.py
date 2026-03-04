from django.urls import path
from . import views

urlpatterns = [
    path('table/<int:table_number>/', views.menu_view, name='menu'),
    path('create-order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_status, name='order_status'),
    path('kitchen/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('update-status/<int:order_id>/<str:new_status>/', views.update_status, name='update_status'),
    path('kitchen-data/', views.kitchen_data, name='kitchen_data'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]