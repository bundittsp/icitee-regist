from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
]
