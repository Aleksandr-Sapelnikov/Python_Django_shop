from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=100)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name!r}"


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        verbose_name_plural = ('Товары')
        verbose_name = ('Товар')

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(null=False, blank=True, verbose_name='Описание')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # reviews =
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name!r} {self.price!r}"


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, verbose_name='Текст отзыва', help_text='Тут Ваш отзыв')
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)

    class Meta:
        verbose_name_plural = ('Отзывы')
        verbose_name = ('Отзыв')

    def __str__(self):
        return f'{self.user} - {self.product}'

    def view_reviews(self):
        return self.text if len(self.text) < 15 else (self.text[:15] + '...')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Покупатель")
    email = models.EmailField(verbose_name='E-mail заказчика')
    fio = models.CharField(max_length=60, verbose_name='ФИО заказчика')
    phone = models.CharField(max_length=18, verbose_name='Телефон заказчика')
    DELIVERY_CHOICE = (
        ('1', 'Обычная доставка'),
        ('2', 'Экспресс доставка'),
    )
    delivery_type = models.CharField(max_length=30, choices=DELIVERY_CHOICE, default='1', verbose_name='Способ доставки')
    city = models.CharField(max_length=30, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    PAYMENT_CHOICE = (
        ('1', 'Картой онлайн'),
        ('2', 'Онлайн со случайного чужого счёта')
    )
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICE, default='1', verbose_name='Способ оплаты')

    # order_item = models.ManyToManyField(OrderItem, blank=True, related_name='order')
    # total_price = models.PositiveIntegerField(default=0, verbose_name="Итоговая цена")
    status = models.BooleanField(default=False, verbose_name='Оплачен')
    created = models.DateTimeField(auto_now_add=True)
    error_text = models.CharField(max_length=100, blank=True, verbose_name='Ошибка')

    # добавить поля стоимости для обычной доставки и для экспресс, чтобы можно было менять в админке.
    # или лучше добавить новую модель с константами и записать туда цены на доставки и в теории можно будет еще что-то
    def __str__(self):
        return "Заказ ({})".format(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_cost(self):
        if self.delivery_type == '1':
            if sum(item.get_cost() for item in self.items.all()) >= 2000:
                return sum(item.get_cost() for item in self.items.all())
            else:
                return sum(item.get_cost() for item in self.items.all()) + 200
        else:
            return sum(item.get_cost() for item in self.items.all()) + 500


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return "Объект: {} (заказ)".format(self.product.name)

    class Meta:
        verbose_name = 'Объект заказа'
        verbose_name_plural = 'Объекты заказа'

    def get_cost(self):
        return self.price * self.quantity
