from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


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
            ('category_image', blocks.ListBlock(ImageBlock(required=True))),
        ])),
        ("trending", blocks.StructBlock([
            ('heading', blocks.CharBlock(required=True)),
            ('card', blocks.ListBlock(blocks.StructBlock([
                ('title', blocks.CharBlock(required=True)),
                ('price', blocks.CharBlock(required=True)),
                ('card_image', ImageBlock(required=True)),
            ]))),
        ]))
    ], blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('widgets'),
        FieldPanel('body'),
    ]
