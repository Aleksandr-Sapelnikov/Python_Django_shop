from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from cart.cart import Cart
from .models import Product, Reviews, Category
from django.views.generic import DetailView, CreateView
from .forms import ReviewsForm


# добавление отзыва и перенаправление обратно на страницу продукта
class AddReviews(CreateView):
    model = Reviews
    template_name = 'shop/product.html'
    form_class = ReviewsForm
    success_url = reverse_lazy('shop:product')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'
    context_object_name = 'product'
    # Тут будет реализована возможность добавления отзыва
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form_add_']

#Добавьте сервис интеграции с сервисом оплаты, создайте методы-заглушки для
# работы этого сервиса. Сервис должен позволять:
# ● оплатить указанный заказ;
# ● получить статус оплаты заказа.
# Опишите эти методы в сервисе и в его интерфейсе, реализуйте возврат
# статичных данных этими методами.


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
