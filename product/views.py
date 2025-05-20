import os
from django.shortcuts import render
from django.conf import settings

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

def collections(request):
    painting_thumb = os.listdir(settings.STATIC_ROOT + "/painting-thumbnails")
    images = []

    page_size = 18
    page_number = int(request.GET.get("page_number", 1))
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    for item in painting_thumb[start_index:end_index]:
        file_name = item.split(".")[0]
        images.append({"name": file_name, "url": "/static/painting-thumbnails/" + item})

    return render(request, "product/collections.html", {"collections": images, "previous": page_number - 1, "next": page_number + 1})