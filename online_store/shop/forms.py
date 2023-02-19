from django import forms
from .models import Reviews, Order
from django.forms import Textarea

DELIVERY_CHOICE = (
        ('1', 'Обычная доставка'),
        ('2', 'Экспресс доставка'),
    )

PAYMENT_CHOICE = (
        ('1', 'Картой онлайн'),
        ('2', 'Онлайн со случайного чужого счёта')
    )


class ReviewsForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('text',)
        exclude = ('user',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fields['text'].widget = Textarea(attrs={'class': "form-textarea",
                                                     'name': 'review',
                                                     'id': 'review',
                                                     'placeholder': 'Review'
                                                     })


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('email', 'fio', 'phone', 'delivery_type', 'city', 'address', 'payment_method',)

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-input'})
        self.fields['fio'].widget = forms.TextInput(attrs={'class': 'form-input'})
        self.fields['phone'].widget = forms.TextInput(attrs={'class': 'form-input'})

        self.fields['delivery_type'].widget = forms.RadioSelect(choices=DELIVERY_CHOICE)
        self.fields['payment_method'].widget = forms.RadioSelect(choices=PAYMENT_CHOICE)

        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-input'})
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-input'})