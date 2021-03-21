from django.urls import path, include

urlpatterns = [
    path('', include('YandexSweets.urls')),
    path('/', include('YandexSweets.urls'))
]
