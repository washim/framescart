import os
import razorpay
from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect
from cms.helper import extract_number_from_parentheses

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from .forms import ShippingForm


class ProductOrder(models.Model):
    order_id = models.CharField(unique=True)
    product_path = models.CharField()
    product_options = models.CharField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    base_price = models.IntegerField()
    paid = models.IntegerField()
    status = models.CharField(choices={"paid": "Paid", "created": "Created", "canceled": "Canceled", "refunded": "Refunded"}, default="paid")
    created = models.DateField(auto_now=True)

    def __str__(self):
        return "Order: " + str(self.order_id)


class ProductPage(RoutablePageMixin, Page):
    description = RichTextField(blank=True)
    summary = RichTextField(blank=True)
    product_rating = models.IntegerField(default=3)
    price = models.IntegerField(default=300)
    widgets = StreamField([
        ("product_images", blocks.ListBlock(ImageBlock(required=True))),
        ("product_options", blocks.ListBlock(blocks.StructBlock([
            ("product_attribute_key", blocks.CharBlock(required=True)),
            ("product_attribute_values", blocks.CharBlock(required=True)),
        ]))),
        ("customer_reviews", blocks.ListBlock(blocks.StructBlock([
            ("name", blocks.CharBlock(required=True)),
            ("comments", blocks.RichTextBlock(required=True)),
            ("ratting_given", blocks.IntegerBlock(required=True)),
            ("customer_verified", blocks.BooleanBlock(required=False)),
            ("customer_location", blocks.CharBlock(required=True)),
        ]))),
        ("breadcrumb", blocks.TextBlock(required=True)),
    ], blank=True, null=True)

    content_panels = Page.content_panels + ["description", "summary", "product_rating", "price", "widgets"]

    key, secret = settings.RAZORPAY_LIVE_KEY
    client = razorpay.Client(auth=(key, secret))

    @path('')
    def product_payment(self, request):
        if request.method == 'POST':
            product_attributes = [item for item in request.POST.keys() if item not in ["csrfmiddlewaretoken", "quantity"]]
            product_values = [request.POST[item] for item in product_attributes]
            total_due = self.price
            
            for record in product_values:
                price_modifier = extract_number_from_parentheses(record)
                total_due += price_modifier
            
            quantity = int(request.POST["quantity"])
            final_due = total_due * quantity
            razorpay_order = self.client.order.create({
                "amount": final_due * 100,
                "currency": "INR",
                "receipt": "New Order",
                "notes": {
                    "product_id": str(self.id),
                    "name": self.title,
                    "base_price": self.price,
                    "paid": final_due * 100,
                    "quantity": quantity,
                    "product_options": ",".join(product_values),
                    "product_url": self.url
                }
            })

            return HttpResponseRedirect(f"{self.url}checkout/{razorpay_order['id']}/")

        return self.render(request)

    @path('checkout/<str:order_id>/')
    def checkout_details(self, request, order_id=None):
        try:
            order_details = self.client.order.fetch(order_id)
            if order_details["id"]:
                return self.render(
                    request, 
                    context_overrides={
                        "order": order_details, 
                        "razorpay_key": self.key,
                        "callback_url": f"{self.url}verify/"
                    }, 
                    template="product/checkout.html"
                )
            
            else:
                return HttpResponseRedirect(self.url)
        
        except Exception:
            return HttpResponseRedirect(self.url)

    @path('verify/')
    def verify_order(self, request):
        payment_id = request.GET.get("razorpay_payment_id")
        order_id = request.GET.get("razorpay_order_id")
        signature = request.GET.get("razorpay_signature")
        
        try:
            self.client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            
            return HttpResponseRedirect(f"{self.url}shipping-details/{order_id}/")
        
        except Exception:
            return HttpResponseRedirect(self.slug)

    @path('shipping-details/<str:order_id>/')
    def shipping_details(self, request, order_id=None):
        form = ShippingForm()
        try:
            order = self.client.order.fetch(order_id)
        except Exception:
            return HttpResponseRedirect(f"{self.url}failed/")
        
        if order.get("id"):
            form = ShippingForm(initial=order["notes"])
        
        if request.method == 'POST':
            form = ShippingForm(request.POST)
            if form.is_valid():
                self.client.order.edit(order_id,{
                    "notes": {
                        "address_line_1": form.cleaned_data["address_line_1"],
                        "address_line_2": form.cleaned_data["address_line_2"],
                        "fullname": form.cleaned_data["fullname"],
                        "city": form.cleaned_data["city"],
                        "state": form.cleaned_data["state"],
                        "pincode": form.cleaned_data["pincode"],
                        "mobile": form.cleaned_data["mobile"],
                        "email": form.cleaned_data["email"],
                    }
                })
                return HttpResponseRedirect(f"{self.url}upload/{order_id}/")
        
        return self.render(request, context_overrides={"form": form}, template="product/shipping.html")

    @path('failed/')
    def failed_order(self, request):
        extra_context = {
            "title": "Order Failed",
            "body": "Order creation failed. Please try again later. <a href='"+self.url+"'>Go Back</a>"
        }
        return self.render(request, context_overrides=extra_context, template="product/result.html")

    @path('upload/<str:order_id>/')
    def upload_personalised_images(self, request, order_id=None):
        context = {
            "order_id": order_id
        }
        file_size_limit = 10 * 1024 * 1024 - 1 #10MB
        if request.method == "POST":
            file = request.FILES.get("file")
            if hasattr(file, 'name'):
                file_name, extension = str(file.name).split(".")
                file_to_upload = os.path.join(settings.MEDIA_ROOT, "user_upload", str(file.name).lower())
                if "png" in str(extension).lower() or "zip" in str(extension).lower():
                    if file.size > file_size_limit:
                        context["error_message"] = "File size allowed maximum 10MB"
                    elif str(file_name).lower() != str(order_id).lower():
                        context["error_message"] = f"Please rename the file. File name should be {order_id}.{extension}"
                    elif os.path.exists(file_to_upload):
                        context["error_message"] = "Not allowed. File already exist. Please send your file in our official whatsapp chat."
                    else:
                        with open(file_to_upload, "wb+") as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)
                        
                        extra_context = {
                            "title": "Order Completed",
                            "body": "Relax. We will notify you when product will dispatch after printing. <a href='/'>Keep Shopping</a>"
                        }
                        
                        return self.render(request, context_overrides=extra_context, template="product/result.html")

                else:
                    context["error_message"] = "Only zip and png files are allowed to upload."


        return self.render(request, context_overrides=context, template="product/upload.html")