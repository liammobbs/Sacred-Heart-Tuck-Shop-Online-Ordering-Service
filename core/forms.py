from django import forms
from django.forms import ModelForm
from .models import *

PAYMENT_CHOICES = (
    ('B', 'Pay with Card (Credit/Debit)'),
    ('C', 'Pay with Cash at Tuck Shop')
)

BREAK_CHOICES =(
    'T', 'Morning Tea'
    'L', 'Lunch'
)

class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ('break_choice',
                  'payment_option')


def create_option_form(self):

    class SelectOptionForm(forms.ModelForm):
        variation_item = forms.ModelChoiceField(queryset=ItemVariation.objects.filter(item=self))

    return SelectOptionForm


# class CouponForm(forms.Form):
#     code = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Promo code',
#         'aria-label': 'Recipient\'s username',
#         'aria-describedby': 'basic-addon2'
#     }))

#
# class RefundForm(forms.Form):
#     ref_code = forms.CharField()
#     message = forms.CharField(widget=forms.Textarea(attrs={
#         'rows': 4
#     }))
#     email = forms.EmailField()

#
# class PaymentForm(forms.Form):
#     stripeToken = forms.CharField(required=False)
#     save = forms.BooleanField(required=False)
#     use_default = forms.BooleanField(required=False)
