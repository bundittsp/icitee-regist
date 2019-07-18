import string
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

# Create your views here.
from django.template.loader import render_to_string
from django.views import View

from regist.forms import PaymentForm, AuthorForm, UserForm, MyUserCreationForm
from regist.models import Article, Payment
from regist.tokens import account_activation_token


def register(request):
    success = False
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        author_form = AuthorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user_form.is_valid():
                user.email = user_form.cleaned_data.get('email')
                user.first_name = user_form.cleaned_data.get('first_name')
                user.last_name = user_form.cleaned_data.get('last_name')
                user.is_staff = False
                user.is_superuser = False
                user.is_active = False
                if author_form.is_valid():
                    user.save()
                    author = author_form.save(commit=False)
                    author.user = user
                    author.save()
                    success = True
                    # Send email with a link to activate account!!!
                    current_site = get_current_site(request)
                    subject = 'ICITEE2019 - account activation'
                    message = render_to_string('email/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': user.pk,
                        'token': account_activation_token.make_token(user),
                    })

                    email = EmailMessage(
                        subject, message, to=[user.email]
                    )
                    email.send()
    else:
        form = MyUserCreationForm()
        user_form = UserForm()
        author_form = AuthorForm()

    return render(request, 'register.html',
                  {
                      'form': form,
                      'author_form': author_form,
                      'user_form': user_form,
                      'success': success
                  })


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
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

    payments = Payment.objects.filter(create_by=request.user)

    return render(
        request,
        template_name='index.html',
        context={
            'articles': articles,
            'payments': payments
        }
    )


class ProfileView(View):
    template_name = 'profile/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = UserForm(instance=user)
        author_form = AuthorForm(instance=user.author)

        return render(request, self.template_name, {
            'user': user,
            'user_form': user_form,
            'author_form': author_form
        })

    def post(self, request, *args, **kwargs):
        success = False
        user = request.user
        user_form = UserForm(request.POST, instance=user)
        author_form = AuthorForm(request.POST, instance=user.author)
        if user_form.is_valid():
            user_form.save()
            if author_form.is_valid():
                author_form.save()
                success = True

        return render(request, self.template_name, {
            'user': user,
            'user_form': user_form,
            'author_form': author_form,
            'success': success
        })


# มติ อัตราค่าลงทะเบียนให้ใช้อัตราเดียวกับ ICITEE 2017 และ ICITEE 2015 ซึ่งทั้ง 2 ครั้งนั้นใช้อัตราเดียวกัน
# โดยให้ประกาศอัตราทั้งหน่วยเงินบาท และ US$ ดังนี้
# - Early bird registration	IEEE/ECTI Member = 12,000 / Non- IEEE/ECTI Member = 14,000
# - Regular registration	IEEE/ECTI Member = 14,000 / Non- IEEE/ECTI Member = 16,000
# - Additional paper = 12,000
# - Extra page (each additional, max. 2 pages) = 2,000
# - Attendant (observer) = 6,000
# - Additional Banquet ticket = 1,500
# ส่วน Special rate สำหรับ UGM กำหนดอัตรา Flat rate 10,000 บาท โดยแจ้งเป็นการภายในให้ทราบเฉพาะ UGM เท่านั้น
class PaymentView(View):
    form_class = PaymentForm
    template_name = 'payment/payment.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(authors__id=request.user.id, is_paid=False)

        form = self.form_class()

        return render(request, self.template_name, {
            'form': form,
            'articles': articles,

        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return render(request, 'payment/credit.html', {'form': form})

        return render(request, 'payment/credit.html', {'form': form})

