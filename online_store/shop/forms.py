from django import forms
from .models import Reviews
from django.forms import Textarea


class ReviewsForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields ='text'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fields['text'].widget = Textarea(attrs={'rows': 5})
