from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product
from django.urls import reverse_lazy


def cart_add_in_catalog(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product)

    return redirect('shop:catalog')


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    # return render(request, 'cart/cart.html', {'cart': cart})
    return render(request, 'cart/detail.html', {'cart': cart})

# def cart_add(request, pk):
#     """Корзина, вариант, который делал сам в домашнем задании, но тут не получиться реализовать все функции"""
#     product_id = str(pk)
#     print('id продукта', product_id)
#
#     if 'cart' not in request.session:
#         request.session['cart'] = dict()
#         request.session['cart'][product_id] = 1
#         print('Корзина новой сессии + добавление в нее', request.session['cart'])
#         request.session.save()
#     elif product_id not in request.session['cart']:
#         request.session['cart'][product_id] = 1
#         request.session.save()
#
#         print('Появление нового ключа')
#     else:
#         prod = Product.objects.get(id=product_id)
#         print(prod.count)
#         if prod.count > request.session['cart'][product_id]:
#             request.session['cart'][product_id] += 1
#             request.session.save()
#         else:
#             print('Достигнут максимум товара, который есть в наличии')
#             request.session['cart'][product_id] = prod.count
#             request.session.save()
#         print('Корзина есть, надо добавлять число', request.session['cart'])
#
#     print(request.session['cart'])
#     return HttpResponseRedirect(reverse_lazy("app_shop:product_list"))
#     # return HttpResponse('Добавлено в корзину')
#
#
# def cart_remove(request, pk):
#     product_id = str(pk)
#     print('id продукта', product_id)
#
#     if product_id in request.session['cart']:
#         del request.session['cart'][product_id]
#         request.session.save()
#
#     return render(request, 'cart/cart.html')
#
#
# def cart_view(request):
#     if 'cart' not in request.session:
#         request.session['cart'] = dict()
#     list_prod = {}
#     total_price = 0
#     for product_id, product_count in request.session['cart'].items():
#         prod = Product.objects.get(id=product_id)
#         price = prod.price
#         total_price += price * product_count
#         list_prod[prod] = product_count
#         print(list_prod)
#
#     context = {
#         'cart': list_prod,
#         'total_price': total_price
#         # 'cart': Product.objects.filter(pk__in=request.session['cart'])
#     }
#     return render(request, 'cart/cart.html', context=context)
#
#
# def cart_clear(request):
#     request.session['cart'].clear()
#     request.session.save()
#     print(request.session['cart'])
#     list_prod = {}
#     total_price = 0
#     context = {
#         'cart': list_prod,
#         'total_price': total_price
#     }
#     return render(request, 'cart/cart.html', context=context)
