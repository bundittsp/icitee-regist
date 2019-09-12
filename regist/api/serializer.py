from django.utils import timezone
from rest_framework import serializers

from regist.models import Payment, AdditionalItem, PaymentItem, Article, Author


class DateTimeFieldWihTZ(serializers.DateTimeField):
    '''
        Class to make output of a DateTime Field timezone aware
    '''
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class AuthorSerializer(serializers.ModelSerializer):
    fname = serializers.ReadOnlyField(source='user.first_name')
    lname = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Author
        fields = ('user', 'fname', 'lname', 'email', 'country')


class PaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentItem
        fields = ('__all__')


class PaymentSerializer(serializers.ModelSerializer):
    create_date = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M', read_only=True)
    paymentitem_set = PaymentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ('__all__')


class ArticleListingField(serializers.RelatedField):
    def to_representation(self, value):
        return '%s %s (%s)' % (value.first_name, value.last_name, value.username)


class ArticleSerializer(serializers.ModelSerializer):
    authors = ArticleListingField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('__all__')


class AdditionalItemSerializer(serializers.ModelSerializer):
    disc_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disc_price_us = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        model = AdditionalItem
        fields = ('__all__')
