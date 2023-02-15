from django import forms
from .models import Reviews
from django.forms import Textarea


class ReviewsForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields =('text',)
        exclude = ('user',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fields['text'].widget = Textarea(attrs={'class': "form-textarea",
                                                     'name': 'review',
                                                     'id': 'review',
                                                     'placeholder': 'Review'
                                                     })
