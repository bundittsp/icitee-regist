from django.urls import path

from . import views

urlpatterns = [
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
]
