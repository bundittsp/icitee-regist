from datetime import date

from django.db import transaction
from django.db.models import Q, F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from regist.api.serializer import AdditionalItemSerializer, ArticleSerializer, PaymentSerializer, PaymentItemSerializer
from regist.models import AdditionalItem, Article


class ArticleListAPIView(APIView):

    def get(self, request):
        articles = Article.objects.filter(authors__id=request.user.id, is_paid=False)
        exclude_ids = []
        for article in articles:
            if article.paymentitem_set.filter(payment__del_flag=False).count() > 0:
                exclude_ids.append(article.id)

        articles = articles.exclude(id__in=exclude_ids)
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdditionalItemListAPIView(APIView):

    def get(self, request):
        # Check is early bird
        is_early = date.today() <= date(2019, 9, 16)
        additions = AdditionalItem.objects.all().annotate(
            disc_price=F('price'),
            disc_price_us=F('price_us')
        )

        for addition in additions:
            if is_early and not (request.user.author.is_ugm or request.user.author.is_jcsi):
                addition.disc_price -= addition.early_disc
                addition.disc_price_us -= addition.early_disc_us
            else:
                # ส่วนลด ugm และ jsci จะไม่สนใจ early bird จ่ายก่อนหรือหลังราคาเท่ากัน
                if request.user.author.is_ugm:
                    addition.disc_price -= addition.ugm_disc + addition.early_disc
                    addition.disc_price_us -= addition.ugm_disc_us + addition.early_disc_us
                if request.user.author.is_jcsi:
                    addition.disc_price -= addition.jsci_disc + addition.early_disc
                    addition.disc_price_us -= addition.jsci_disc_us + addition.early_disc_us

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
        is_member = request.data.get('is_member')
        selected = request.data.get('selected')
        print(selected)

        # Create payment
        data = {
            'remark': remark,
            'address': address,
            'method': method,
            'currency': currency,
            'create_by': request.user.id,
            'member': is_member
        }
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            payment = serializer.save()
            payment.code = "{:06d}".format(payment.id)
            payment.save()

            for product in products:
                # Create payment items -> for main paper
                if product['id'] in [1, 2]:
                    data = {
                        'payment': payment.id,
                        'article': selected[0],
                        'add_item': product['id'],
                        'amount': product['amount'],
                        'price': product['disc_price'] if currency == 'THB' else 0,
                        'price_us': product['disc_price_us'] if currency == 'USD' else 0,
                    }
                    item_serializer = PaymentItemSerializer(data=data)
                    if item_serializer.is_valid():
                        item_serializer.save()
                    else:
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # Create payment items -> for add papers
                elif product['id'] == 3:
                    for i in range(1, product['amount'] + 1):
                        data = {
                            'payment': payment.id,
                            'article': selected[i],
                            'add_item': product['id'],
                            'amount': 1,
                            'price': product['disc_price'] if currency == 'THB' else 0,
                            'price_us': product['disc_price_us'] if currency == 'USD' else 0,
                        }
                        item_serializer = PaymentItemSerializer(data=data)
                        if item_serializer.is_valid():
                            item_serializer.save()
                        else:
                            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # Create payment items -> for extra pages, attendant, banquet
                elif product['id'] > 3:
                    data = {
                        'payment': payment.id,
                        'article': None,
                        'add_item': product['id'],
                        'amount': product['amount'],
                        'price': product['disc_price'] if currency == 'THB' else 0,
                        'price_us': product['disc_price_us'] if currency == 'USD' else 0,
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


