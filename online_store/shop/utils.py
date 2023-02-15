

def reduce_quantity_product(prod, quantity):
    """Уменьшение количества продуктов"""
    # prod = Product.objects.get(id=product_id)
    print(f'{prod.name} - Количество в наличии: {prod.quantity}')
    prod.quantity -= quantity
    prod.save()

    print(f'{prod.name} - Количество после: {prod.quantity}')


def change_order_status(order):
    """Изменение статуса заказа"""
    # order = Order.objects.get(id=order_id)
    order.status = True
    order.save()
    print(order.id, 'Статус изменен на "Оплачен"')
    # можно добавить запрос всех заказов со статусом False, и их удаление в цикле (на случай если создался лишний заказ)
