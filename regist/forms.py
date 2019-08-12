import os
from uuid import uuid4

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField

from regist.models import Payment, Author


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'






class UploadSlipForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadSlipForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'accept': '.jpg, .png, .pdf'})


class SearchPaymentForm(forms.Form):
    name_text = forms.CharField(max_length=200, required=False)
    METHODS = (
        ('', '--------'),
        ('C', 'Credit Card'),
        ('T', 'Bank Transfer'),
    )
    method = forms.ChoiceField(choices=METHODS, required=False)
    CURRENCIES = [
        ('', '-----'),
        ('THB', 'THB'),
        ('USD', 'USD')
    ]
    currency = forms.ChoiceField(choices=CURRENCIES, required=False)
    confirm = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchPaymentForm, self).__init__(*args, **kwargs)
        self.fields['name_text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'EDAS ID, Title'})
        self.fields['method'].widget.attrs.update({'class': 'form-control'})
        self.fields['currency'].widget.attrs.update({'class': 'form-control'})


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your EDAS ID*'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password*'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat Password*'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name*'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name*'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email*'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and username and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email address is already registered.')
        return email


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('country', 'ieee')

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['ieee'].widget.attrs.update({'class': 'form-control', 'placeholder': 'IEEE No.'})
