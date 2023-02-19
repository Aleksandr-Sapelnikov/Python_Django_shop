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
]