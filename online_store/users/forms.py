from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(required=False, max_length=10, label='Телефон',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    fio = forms.CharField(required=False, max_length=60, label='ФИО',
                          widget=forms.TextInput(attrs={'class': 'form-input'}))
    p_img = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'Profile-file form-input'}))

    class Meta:
        model = Profile
        fields = ('phone', 'fio', 'p_img')
# <input class="Profile-file form-input" id="avatar" name="avatar" type="file" data-validate="onlyImgAvatar">