from django.shortcuts import render

from wagtail.admin.viewsets.model import ModelViewSet
from .models import ProductOrder


class ProductOrderViewSet(ModelViewSet):
    model = ProductOrder
    exclude_form_fields = ["created"]
    list_display = ["order_id", "product_path", "product_options", "quantity", "base_price", "paid", "status"]
    icon = "date"
    add_to_admin_menu = True
    copy_view_enabled = False
    inspect_view_enabled = True


product_order_viewset = ProductOrderViewSet("orders")
