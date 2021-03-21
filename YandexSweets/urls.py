from django.urls import path

from YandexSweets import views

urlpatterns = [
    path('couriers', views.CouriersView.as_view()),
    path('couriers/<int:c_id>', views.CouriersView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/assign', views.OrdersAssignView.as_view()),
    path('orders/complete', views.OrdersCompleteView.as_view())
]
