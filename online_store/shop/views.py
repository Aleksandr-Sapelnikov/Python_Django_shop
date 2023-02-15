from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, FormView
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Product, Reviews, Category
from django.views.generic import DetailView, CreateView, ListView
from .forms import ReviewsForm
from .filters import ProductFilter


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
        queryset = Product.objects.filter(category__slug=self.kwargs['cat_slug'])
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        print(self.kwargs)
        # category = Category.objects.filter()

        return context


@login_required
def order_create(request):
    """Создание заказа из корзины"""
    cart = Cart(request)
    list_prod = {}
    total_price = 0
    pass
    # Пока точно не проверил корзину, но нужно брать продукты из корзины, создать инстанс заказа или взять существующий

    # for product_id, product_count in request.session['cart'].items():
    #     prod = Product.objects.get(id=product_id)
    #     price = prod.price
    #     total_price += price * product_count
    #     list_prod[prod] = product_count
    #     print(list_prod)
    #
    # try:
    #     # instance = (Order.objects.prefetch_related("products").filter(status=False).get(user=request.user))
    #     instance = (Order.objects.filter(status=False, user=request.user).first()) # как вариант для взятия первого
    #     # instance = (Order.objects.filter(status=False).get(user=request.user))
    #     print('Уже есть запись в базе', instance)
    #     instance.products.set(list_prod)
    #     instance.total_price = total_price
    #     instance.save()
    #     print('Обновленная запись', instance)
    #     dict_to_str = json.dumps(request.session['cart'])
    #     new_dict = OrderDict.objects.get(order_id=instance.id)
    #     new_dict.cart_dict = dict_to_str
    #     new_dict.save()
    #     print('Словарь', new_dict)
    #     print(json.loads(dict_to_str))
    #
    # # except ObjectDoesNotExist:
    # except AttributeError:
    #     instance = Order(user=request.user, total_price=total_price)
    #     instance.save()
    #     instance.products.set(list_prod)
    #     instance.save()
    #     print('Создан заказ', instance)
    #     dict_to_str = json.dumps(request.session['cart'])
    #     new_dict = OrderDict(cart_dict=dict_to_str, order_id=instance.id)
    #     new_dict.save()
    #     print('Словарь', new_dict)
    #
    # context = {
    #     'cart': list_prod,
    #     'total_price': total_price,
    #     'order': instance
    #
    # }
    # return render(request, 'app_shop/order.html', context=context)


@login_required
def order_payment(request, pk):
    """Оплата заказа указанного заказа"""
    pass
    # order_id = int(pk)
    # order_dict = OrderDict.objects.get(order_id=order_id)
    # order = (Order.objects.prefetch_related("products").get(id=order_id))
    # # order = Order.objects.select_related("user").prefetch_related("products").filter(id=order_id, status=False)
    # # order = (Product.objects.prefetch_related("order").filter(id=order_id).filter(status=False).all())
    # print('заказ', order)
    # products = order.products
    # print(products)
    # print(order.total_price)
    # print(order.products.all())
    # print(json.loads(order_dict.cart_dict))
    # list_prod = {}
    # total_price = 0
    # try:
    #     with transaction.atomic():
    #         for product_id, product_count in json.loads(order_dict.cart_dict).items():
    #             prod = Product.objects.get(id=product_id)
    #             reduce_quantity_product(prod=prod, count=product_count)
    #             price = prod.price
    #             total_price += price * product_count
    #             list_prod[prod] = product_count
    #         print(list_prod)
    #         print(total_price)
    #
    #         change_order_status(order)
    #
    #         reduce_user_balance(user=request.user, total_price=total_price)
    #         request.session['cart'].clear()
    #         request.session.save()
    #         # return HttpResponse('Успех!!!')
    #         order_dict.delete()
    #         log.info('Оформление заказа')
    #         return HttpResponseRedirect(reverse_lazy("app_shop:product_list"))
    #
    # except Exception:
    #     return HttpResponse('Что-то пошло не так. Возможно стоит проверить баланс? Возможно закончился товар.')
