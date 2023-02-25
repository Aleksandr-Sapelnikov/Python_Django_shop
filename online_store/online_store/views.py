from django.shortcuts import render
from django.views import View
from shop.models import Category, Product
from django.db.models import Count


class BaseView(View):

    def get(self, request):
        # category = Category.objects.select_related('parent').all().order_by('name')
        first_item = Product.objects.all()[:8]
        limited_item = Product.objects.all().order_by('quantity')[:16]
        # categories = Category.objects.annotate(one=Count('category')).filter(one__gt=0)
        context = {
            'first_8_item': first_item,
            'limited_item': limited_item
        }
        return render(request, 'index.html', context)
