from datetime import date
from pprint import pprint

from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from regist.api.serializer import AdditionalItemSerializer, ArticleSerializer, PaymentSerializer, PaymentItemSerializer
from regist.models import AdditionalItem, Article


class ArticleListAPIView(APIView):

    def get(self, request):
        articles = Article.objects.filter(authors__id=request.user.id, is_paid=False, paymentitem__isnull=True)
        serializer = ArticleSerializer(articles, many=True)

        # Check is early bird
        is_early = date.today() <= date(2019, 9, 10)

        return Response({'articles': serializer.data, 'is_early': is_early}, status=status.HTTP_200_OK)


class AdditionalItemListAPIView(APIView):

    def get(self, request):
        articles = Article.objects.filter(authors__id=request.user.id, is_paid=False)

        if articles.filter(authors__author__is_ugm=True).exists():
            additions = AdditionalItem.objects.all()
        else:
            additions = AdditionalItem.objects.filter(~Q(name='UGM discount'))

        # Check is early bird
        is_early = date.today() <= date(2019, 9, 10)
        if not is_early:
            additions.exclude(name='Early bird discount')

        serializer = AdditionalItemSerializer(additions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentCreateAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        # Get data
        products = request.data.get('products')
        method = request.data.get('method', 'T')
        currency = request.data.get('currency', 'THB')
        address = request.data.get('address')
        remark = request.data.get('remark')

        # Create payment
        data = {
            'remark': remark,
            'address': address,
            'method': method,
            'currency': currency,
            'create_by': request.user.id
        }
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            payment = serializer.save()
            payment.code = "{:06d}".format(payment.id)
            payment.save()

            # Create payment items
            pprint(products)
            for product in products:
                data = {
                    'payment': payment.id,
                    'article': product['article'] if product['article'] > 0 else None,
                    'add_item': product['id'],
                    'amount': product['amount'],
                    'price': product['price'] if currency == 'THB' else 0,
                    'price_us': product['price_us'] if currency == 'USD' else 0,
                }
                item_serializer = PaymentItemSerializer(data=data)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update is_paid -> article
        return Response(serializer.data, status=status.HTTP_201_CREATED)


