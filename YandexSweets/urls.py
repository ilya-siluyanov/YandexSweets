from django.urls import path

from YandexSweets import views

urlpatterns = [
    path('couriers', views.Couriers.as_view()),
    path('couriers/<int:c_id>', views.Couriers.as_view()),
    path('orders', views.Orders.as_view()),
    path('orders/assign', views.OrdersAssign.as_view()),
    path('orders/complete', views.OrdersComplete.as_view)
]
