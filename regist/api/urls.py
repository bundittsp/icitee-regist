from django.urls import path

from . import views

urlpatterns = [
# SHOW payment detail
    # path('payment/<int:payment_id>/manage/', views.PaymentManageAPIView.as_view(), name='payment-manage'),
    # SAVE payment
    path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),

    path('payment/article-list/', views.ArticleListAPIView.as_view(), name='article-list'),
    path('payment/addition-list/', views.AdditionalItemListAPIView.as_view(), name='addition-list'),
]
