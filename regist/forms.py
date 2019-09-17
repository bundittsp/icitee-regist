import os
from uuid import uuid4

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField

from regist.models import Payment, Author, Article


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class UploadFileForm(forms.Form):
    slip = forms.FileField(required=False)
    ieee = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['slip'].widget.attrs.update({'class': 'form-control', 'accept': '.jpg, .png, .pdf'})
        self.fields['ieee'].widget.attrs.update({'class': 'form-control', 'accept': '.jpg, .png, .pdf'})


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
    confirm = forms.BooleanField(initial=False, required=False, label='Is confirmed?')
    slip = forms.BooleanField(initial=False, required=False, label='Upload slip?')
    ieee = forms.BooleanField(initial=False, required=False, label='IEEE membership?')

    def __init__(self, *args, **kwargs):
        super(SearchPaymentForm, self).__init__(*args, **kwargs)
        self.fields['name_text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'EDAS ID, Title'})
        self.fields['method'].widget.attrs.update({'class': 'form-control'})
        self.fields['currency'].widget.attrs.update({'class': 'form-control'})


# class MyUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your EDAS ID*'})
#         self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password*'})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat Password*'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your EDAS ID (Author ID)*'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your EDAS account email*'})

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        try:
            if email and username:
                User.objects.get(email=email, username=username)
            else:
                raise forms.ValidationError(u'Please input both EDAS ID and email')
        except User.DoesNotExist:
            raise forms.ValidationError(u'Cannot find your information please contact icitee2019.it.kmitl.ac.th')

        return email


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('country', )

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control'})


# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         exclude = ('is_paid', 'authors')
