from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import RegisterForm, ProfileUpdateForm
from .models import Profile
from shop.models import Order


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('/')

    # def get_success_url(self):
    #     print('путь', self.request.META.get('HTTP_REFERER'))
    #     return self.request.META.get('HTTP_REFERER')


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


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/account.html'
    model = User
    context_object_name = "user"

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_order'] = Order.objects.filter(user=self.object).order_by('-created')[0]
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    model = Profile
    form_class = ProfileUpdateForm


    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     super().dispatch(request, *args, **kwargs)
    # def get_success_url(self):
    #     return reverse_lazy('users:account', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if user.is_authenticated:
        #     print('Авторизован')
        # else:
        #     print('не авторизован')
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile,
                                                    initial={'fio': user.profile.fio,
                                                             'phone': user.profile.phone,
                                                             'email': user.email,
                                                             'p_img': user.profile.p_img})
        return context

    def form_valid(self, form):
        fio = form.cleaned_data['fio']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        p_img = form.cleaned_data['p_img']
        profile = form.save(commit=False)
        user = profile.user
        user.email = email
        user.save()
        profile.save()
        return HttpResponseRedirect(reverse_lazy('users:account', kwargs={'pk': self.get_object().id}))


