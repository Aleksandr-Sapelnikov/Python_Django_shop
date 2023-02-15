from django import template
from shop.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.select_related('parent').all().order_by('name')
