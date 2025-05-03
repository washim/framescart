from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class  CustomFormBuilder(FormBuilder):
    def get_create_field_function(self, type):
        create_field_function = super().get_create_field_function(type)

        def wrapped_create_field_function(field, options):
            created_field = create_field_function(field, options)
            created_field.widget.attrs.update({
                "class": field.field_classname,
                "placeholder": field.placeholder,
            })
            
            return created_field
    
        return wrapped_create_field_function


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')
    field_classname = models.CharField("Field classes", blank=True, null=True)
    placeholder = models.CharField("Placeholder", blank=True, null=True, default="")

    panels = AbstractFormField.panels + [
        FieldPanel("field_classname"),
        FieldPanel("placeholder"),
    ]


class FormPage(AbstractEmailForm):
    form_builder = CustomFormBuilder
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


class ArticlePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]