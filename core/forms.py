from django import forms
from django.forms import ModelForm
from .models import Order, UserProfile

PAYMENT_CHOICES = (
    ('B', 'Pay with Card (Credit/Debit)'),
    ('C', 'Pay with Cash at Tuck Shop')
)

BREAK_CHOICES =(
    'T', 'Morning Tea'
    'L', 'Lunch'
)
class TopupForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('balance',)

class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ('break_choice',
                  'payment_option')


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

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
