from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegisterView, UserSetPassword, UserSetPasswordDone


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('set_password/', UserSetPassword.as_view(), name='set_password'),
    path('set_password/done', UserSetPasswordDone.as_view(), name='set_password_done'),
    #path('profile/<int:pk>', UserUpdateView.as_view(), name='profile_update'),
]