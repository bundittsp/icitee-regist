from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    edas_id = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    remark = models.CharField(max_length=200, blank=True, null=True)
    page_no = models.IntegerField(blank=True, null=True)
    authors = models.ManyToManyField(User)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_us = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ieee = models.CharField(max_length=20, blank=True, null=True)
    is_ugm = models.BooleanField(default=False)


class AdditionalItem(models.Model):
    name = models.CharField(max_length=50)
    remark = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_us = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Payment(models.Model):
    code = models.CharField(max_length=20)
    remark = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    METHODS = (
        ('C', 'Credit Card'),
        ('T', 'Bank Transfer'),
    )
    method = models.CharField(max_length=1, choices=METHODS)
    slip = models.ImageField(upload_to='slips/', null=True, blank=True)
    del_flag = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_create_by')
    delete_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_delete_by')


class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    add_item = models.ForeignKey(AdditionalItem, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    CURRENCIES = (
        ('THB', 'Thai Baht'),
        ('USD', 'US Dollar'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCIES)

