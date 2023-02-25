from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = 'shop'

urlpatterns = [
    path('<slug:cat_slug>', views.ProductCategory.as_view(), name='category'),
    path('', views.ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('product/<int:pk>/review', require_POST(views.AddReviews.as_view()), name='review'),
    path('order/create', views.OrderCreateView.as_view(), name='order_create'),
    path('order/payment/<int:pk>/', views.payment, name='order_pay'),
    path('order/progresspay', views.progress_pay, name='progress_pay'),
    path('order/history', views.OrderHistoryView.as_view(), name='order_history'),
    path('order/detail/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]