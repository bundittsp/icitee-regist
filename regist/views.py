import string
import random
from distutils.util import strtobool

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum, F, DecimalField
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage

# Create your views here.
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from regist.forms import AuthorForm, UserForm, SearchPaymentForm, UploadSlipForm
from regist.models import Article, Payment, Author
from regist.tokens import account_activation_token


def register(request):
    success = False
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username').strip())
        if user and not user.is_active:
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                success = True
                # Send email with a link to activate account!!!
                letters_and_digits = string.ascii_letters + string.digits
                password = ''.join(random.choice(letters_and_digits) for i in range(8))
                # Update user password
                user.set_password(password)
                user.save()
                current_site = get_current_site(request)
                subject = 'ICITEE2019 - account activation'
                message = render_to_string('email/acc_active_email.html', {
                    'user': user,
                    'password': password,
                    'domain': current_site.domain,
                    'uid': user.pk,
                    'token': account_activation_token.make_token(user),
                })

                email = EmailMessage(
                    subject, message, to=[user.email]
                )
                email.send()
        elif user and user.is_active:
            form = UserForm(request.POST, instance=user)
            form.add_error(field=None, error=ValidationError('The account has already been created.', code='invalid'))
        else:
            form = UserForm(request.POST)
            form.add_error(field=None, error=ValidationError('Cannot find a matching record.', code='invalid'))
    else:
        form = UserForm()

    return render(request, 'register.html',
                  {
                      'form': form,
                      'success': success
                  })


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        try:
            author = user.author
        except Author.DoesNotExist:
            user.author = Author.objects.create()

        user.save()

        login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def forget_password(request):
    success = False
    message = ''
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))

            # Send email with a new password!!!
            subject = 'ICITEE2019 - reset password'

            letters_and_digits = string.ascii_letters + string.digits
            new_pass = ''.join(random.choice(letters_and_digits) for i in range(8))
            user.set_password(new_pass)
            user.save()

            message = render_to_string('email/forget_password_email.html', {
                'user': user,
                'password': new_pass
            })

            email = EmailMessage(
                subject, message, to=[request.POST.get('email')]
            )
            email.send()
            success = True
            message = 'We have sent you a new password, please check you email.'
        except User.DoesNotExist:
            message = 'We cannot find your email. Please create an account.'

    return render(request, template_name='forget-password.html', context={'success': success, 'message': message})


@login_required
def index(request):
    articles = Article.objects.filter(authors__id=request.user.id)

    payments = Payment.objects.filter(create_by=request.user, del_flag=False).annotate(
        total=Sum(F('paymentitem__price') * F('paymentitem__amount'),
                  output_field=DecimalField(max_digits=10, decimal_places=2)),
        total_us=Sum(F('paymentitem__price_us') * F('paymentitem__amount'),
                     output_field=DecimalField(max_digits=10, decimal_places=2)),
    )

    return render(
        request,
        template_name='index.html',
        context={
            'articles': articles,
            'payments': payments
        }
    )


# มติ อัตราค่าลงทะเบียนให้ใช้อัตราเดียวกับ ICITEE 2017 และ ICITEE 2015 ซึ่งทั้ง 2 ครั้งนั้นใช้อัตราเดียวกัน
# โดยให้ประกาศอัตราทั้งหน่วยเงินบาท และ US$ ดังนี้
# - Early bird registration	IEEE/ECTI Member = 12,000 / Non- IEEE/ECTI Member = 14,000
# - Regular registration	IEEE/ECTI Member = 14,000 / Non- IEEE/ECTI Member = 16,000
# - Additional paper = 12,000
# - Extra page (each additional, max. 2 pages) = 2,000
# - Attendant (observer) = 6,000
# - Additional Banquet ticket = 1,500
# ส่วน Special rate สำหรับ UGM กำหนดอัตรา Flat rate 10,000 บาท โดยแจ้งเป็นการภายในให้ทราบเฉพาะ UGM เท่านั้น
@login_required
def payment(request):
    return render(request, 'payment/payment.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def payment_search(request):
    form = SearchPaymentForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data.get('name_text')
        method = form.cleaned_data.get('method')
        currency = form.cleaned_data.get('currency')
        confirm = form.cleaned_data.get('confirm')

        query = [Q(del_flag=False)]
        if name:
            query.append(
                Q(paymentitem__article__edas_id=name) |
                Q(paymentitem__article__title__icontain=name))
        if method:
            query.append(Q(method=method))
        if currency:
            query.append(Q(currency=currency))
        if confirm:
            query.append(Q(confirm=confirm))

        payments = Payment.objects.filter(*query)
    else:
        payments = Payment.objects.all()

    payments = payments.annotate(
            total=Sum('paymentitem__price'), total_us=Sum('paymentitem__price_us')
        ).values(
            'id', 'code', 'total', 'total_us', 'method', 'slip', 'currency',
            'create_by__first_name', 'create_by__last_name',
            'create_date__date', 'confirm'
        ).distinct()

    return render(request, 'payment/search.html', context={
        'form': form,
        'payments': payments
    })


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    if payment.currency == 'THB':
        total_price = payment.paymentitem_set.aggregate(Sum('price'))['price__sum']
    elif payment.currency == 'USD':
        total_price = payment.paymentitem_set.aggregate(Sum('price_us'))['price_us__sum']

    if request.method == 'POST':
        form = UploadSlipForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            payment.slip = file
            payment.save()
    else:
        form = UploadSlipForm()

    if payment.slip:
        payment.slip.name = payment.slip.name[7:]

    return render(request, 'payment/detail.html', {
        'form': form,
        'payment': payment,
        'total_price': total_price
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def payment_confirm(request, payment_id):
    confirm = request.GET.get('confirm', 'false')
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.confirm = strtobool(confirm)
    payment.save()

    # Update is_paid -> articles in payment
    for item in payment.paymentitem_set.all():
        if item.article:
            item.article.is_paid = strtobool(confirm)
            item.article.save()

    return redirect('payment-detail', payment_id=payment_id)

@login_required
def print_confirm(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, del_flag=False)
    total = payment.paymentitem_set.all().aggregate(sum_thb=Sum('price'), sum_usd=Sum('price_us'))

    return render(request, 'payment/print/confirm.html', {
        'payment': payment,
        'total': total['sum_thb'],
        'total_us': total['sum_usd'],
    })


@login_required
def payment_delete(request, payment_id):
    pay = get_object_or_404(Payment, pk=payment_id, del_flag=False)
    pay.del_flag = True
    pay.delete_by = request.user
    pay.save()

    return redirect('index')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'profile/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        author_form = AuthorForm(instance=user.author)

        return render(request, self.template_name, {
            'user': user,
            'author_form': author_form
        })

    def post(self, request, *args, **kwargs):
        success = False
        user = request.user
        author_form = AuthorForm(request.POST, instance=user.author)
        if author_form.is_valid():
            author_form.save()
            success = True

        return render(request, self.template_name, {
            'user': user,
            'author_form': author_form,
            'success': success
        })
