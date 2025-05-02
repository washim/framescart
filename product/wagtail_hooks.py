from wagtail import hooks

from .views import product_order_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return product_order_viewset