from django.urls import path

from . import views

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('payment/search/', views.payment_search, name='payment-search'),
    path('payment/<int:payment_id>/print/confirm/', views.print_confirm, name='payment-print-confirm'),
    path('payment/<int:payment_id>/print/receipt/', views.payment_search, name='payment-print-receipt'),
    path('payment/<int:payment_id>/detail/', views.payment_detail, name='payment-detail'),
    path('payment/<int:payment_id>/delete/', views.payment_delete, name='payment-delete'),
    path('profile/', views.ProfileView.as_view(), name='my-profile'),
]
