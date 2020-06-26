from django.urls import path

from . import views

urlpatterns = [
    path('', views.buy, name='buy'),
    path('buy/', views.buy, name='buy'),
    path('buy-action/', views.buy_action, name='buy-action'),
]
