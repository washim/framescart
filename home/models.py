from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from product.models import ProductPage


@register_setting
class RawHtml(BaseGenericSetting):
    header = models.TextField()
    footer = models.TextField()


class HomePage(Page):
    widgets = StreamField([
        ("carousel_image", blocks.ListBlock(ImageBlock())),
        ("product_search", blocks.BooleanBlock()),
        ("personalised_category", blocks.StructBlock([
            ('heading', blocks.CharBlock(required=True)),
            ('category_image', blocks.ListBlock(blocks.StructBlock([
                ("picture", ImageBlock(required=True)),
                ("pages", blocks.PageChooserBlock(required=False)),
            ]))),
        ])),
        ("trending", blocks.StructBlock([
            ('heading', blocks.CharBlock(required=True)),
            ('pages', blocks.ListBlock(blocks.PageChooserBlock(required=False))),
        ])),
        ("synod", blocks.StructBlock([
            ('heading', blocks.CharBlock(required=True)),
            ('tag', blocks.CharBlock(required=True)),
        ])),
        ("html_panels", blocks.TextBlock(required=True)),
    ], blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('widgets'),
        FieldPanel('body'),
    ]