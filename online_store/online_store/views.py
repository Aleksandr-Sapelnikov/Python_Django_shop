from django.shortcuts import render
from django.views import View
from shop.models import Category
from django.db.models import Count


class BaseView(View):

    def get(self, request):
        # category = Category.objects.select_related('parent').all().order_by('name')

        # categories = Category.objects.annotate(one=Count('category')).filter(one__gt=0)
        return render(request, 'index.html')
