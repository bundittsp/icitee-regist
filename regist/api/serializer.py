from django.utils import timezone
from rest_framework import serializers

from regist.models import Payment, AdditionalItem, PaymentItem, Article


class DateTimeFieldWihTZ(serializers.DateTimeField):
    '''
        Class to make output of a DateTime Field timezone aware
    '''
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class PaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentItem
        fields = ('__all__')


class PaymentSerializer(serializers.ModelSerializer):
    paymentitem_set = PaymentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ('__all__')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('__all__')


class AdditionalItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalItem
        fields = ('__all__')
