from django import template
from product.models import ProductPage

register = template.Library()

@register.simple_tag
def load_synod_pages(tag):
    return ProductPage.objects.filter(tags__name=tag)