from django.forms import ModelForm

from regist.models import Payment


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
