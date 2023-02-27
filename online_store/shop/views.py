from time import sleep

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormMixin, FormView
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Product, Reviews, Category, Order, OrderItem
from django.views.generic import DetailView, CreateView, ListView
from .forms import ReviewsForm, OrderForm, PayForm
from .filters import ProductFilter
from shop.api import OrderAPIUpdate
import requests
from rest_framework.authtoken.models import Token
from django.contrib import messages
from online_store.config import URL_API


# добавление отзыва и перенаправление обратно на страницу продукта
class AddReviews(FormView):
    model = Reviews
    template_name = 'shop/product.html'
    form_class = ReviewsForm
    # success_url = reverse_lazy('shop:product', kwargs=pk)

    def form_valid(self, form):
        print(self.kwargs)
        form_valid = super().form_valid(form)
        obj = form.save(commit=False)
        obj.user = User.objects.get(id=self.request.user.id)
        obj.product = Product.objects.get(id=self.kwargs['pk'])
        obj.save()
        return form_valid

    def get_success_url(self):
        return reverse_lazy('shop:product', kwargs={'pk': self.kwargs['pk']})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewsForm()
        context['cart_form'] = CartAddProductForm()

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    paginate_by = 4
    context_object_name = 'products'

    def get_ordering(self):
        ordering = self.request.GET.get('sorting')

        print(ordering)
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        # if self.ordering:
        #     context['ordering'] = self.ordering
        #     print(self.ordering)
        # print(context)
        # category = Category.objects.filter()

        return context
    # есть проблема (малая) сброс страниц и сортировки при смене фильтра,
    # но фильтр не сбрасывается при сортировке и смене страниц


class ProductCategory(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    paginate_by = 4
    context_object_name = 'products'

    def get_ordering(self):
        ordering = self.request.GET.get('sorting')
        print(ordering)
        return ordering

    def get_queryset(self):
        order = self.get_ordering()
        if order:
            queryset = Product.objects.filter(category__slug=self.kwargs['cat_slug']).order_by(order)
        else:
            queryset = Product.objects.filter(category__slug=self.kwargs['cat_slug']).order_by('name')
        # Product.objects.filter(name__startswith='')
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        print(self.kwargs)
        # category = Category.objects.filter()

        return context


class OrderCreateView(FormView):
    model = Order
    template_name = 'shop/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('base')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['order_form'] = OrderForm(initial={'fio': user.profile.fio,
                                                             'phone': user.profile.phone,
                                                             'email': user.email})
            print('Авторизован')
        else:
            context['order_form'] = OrderForm()
            print('не авторизован')
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        print('заказ', order)
        print('корзина', cart)
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            print('создан объект заказа')
        cart.clear()
        return HttpResponseRedirect(reverse_lazy('shop:order_pay', kwargs={'pk': order.id }))


@login_required
def payment(request, pk):

    if request.method == 'GET':
        form = PayForm()
        order = Order.objects.get(id=pk)
        user = order.user
        print(user)
        print(request.user)
        if user != request.user:
            return HttpResponse('Это не Ваш заказ') # как вариант можно перенаправить на свои заказы

    if request.method == 'POST':
        form = PayForm(request.POST)
        order = Order.objects.get(id=pk)
        user = order.user
        print(user)
        print(request.user)
        if user == request.user:
            if form.is_valid():
                card_num = form.cleaned_data.get('card_num')
                s = requests.Session()
                Token.objects.get_or_create(user=request.user)
                token = Token.objects.get(user=request.user)

                s.headers = {'Authorization': 'Token ' + token.key}
                print(s.headers)
                url = URL_API.format(str(pk))

                r = s.post(url, json={"card_num": card_num})
                print('++++++++++++++++++++++++++++++++++++++post', r.status_code)
                print(r.text)

            return HttpResponseRedirect(reverse_lazy('shop:progress_pay'))
        else:
            return HttpResponse('Это не Ваш заказ') # как вариант можно перенаправить на свои заказы

    context = {
        'pay_form': PayForm()
    }
    return render(request, 'shop/paymentsomeone.html', context)


def progress_pay(request):

    if request.method == 'GET':
        # return HttpResponseRedirect(reverse_lazy('users:account', kwargs={'pk': request.user.id}))
        return render(request, 'shop/progressPayment.html')
    return render(request, 'shop/progressPayment.html')


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/historyorder.html'
    paginate_by = 3
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-created')

        return queryset


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/oneorder.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_item'] = OrderItem.objects.filter(order=self.object)
        return context
