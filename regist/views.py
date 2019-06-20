from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.views import View

from regist.forms import PaymentForm


def login(request):
    return render(request, template_name='regist/login.html', context={})


def logout(request):
    return render(request, template_name='regist/login.html', context={})


def index(request):
    return render(request, template_name='regist/index.html', context={})


class PaymentView(View):
    form_class = PaymentForm
    template_name = 'regist/payment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return render(request, 'regist/credit.html', {'form': form})

        return render(request, 'regist/credit.html', {'form': form})
