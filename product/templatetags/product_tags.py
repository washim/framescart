from django import template
from product.models import ProductPage

register = template.Library()

@register.simple_tag
def get_attribute_values(text):
    data = text.split(",")
    return data

@register.simple_tag
def generate_upload_box(value):
    return [item+1 for item in range(int(value))]

@register.simple_tag
def load_synod_pages(tag):
    return ProductPage.objects.filter(tags__name=tag)