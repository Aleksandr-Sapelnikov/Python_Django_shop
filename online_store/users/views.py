from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import RegisterForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('/')


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    success_url = reverse_lazy('/')


class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('base')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return form_valid


class UserSetPassword(PasswordChangeView):
    template_name = 'users/set_password.html'
    success_url = reverse_lazy('users:set_password_done')


class UserSetPasswordDone(PasswordChangeDoneView):
    template_name = 'users/set_password_done.html'
    success_url = reverse_lazy('base')
