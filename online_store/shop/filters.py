import django_filters
from django_filters.widgets import RangeWidget

from .models import Product


class MyRangeWidget(django_filters.widgets.RangeWidget):

    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class ProductFilter(django_filters.FilterSet):
    # price = django_filters.RangeFilter(widget=RangeWidget(attrs={
    #     'class': "range-line",
    #     'id': 'price',
    #     'name': 'price',
    #     'type': 'text',
    #     'data-type': 'double',
    #     'data-min': '0',
    #     'data-max': '999999',
    #     'data-from': '100',
    #     'data-to': '100000',
    # }))
    price = django_filters.RangeFilter(
    label='Цена',
    widget=MyRangeWidget(
        from_attrs={'placeholder': 'от'},
        to_attrs={'placeholder': 'до'},
    )
)
    # name = django_filters.CharFilter(lookup_expr='istartswith', widget=Link)
    class Meta:
        model = Product
        fields = {
            'name': ['istartswith']
            # 'category__slug': ['icontains']
            # 'category__name': ['icontains']
        }
# class="form-input form-input_full" id="title" name="title" type="text" placeholder="Название"