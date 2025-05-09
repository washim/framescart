# Generated by Django 5.2 on 2025-05-02 10:50

import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(unique=True)),
                ('product_path', models.CharField()),
                ('product_options', models.CharField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('base_price', models.IntegerField()),
                ('paid', models.IntegerField()),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('created', 'Created'), ('canceled', 'Canceled'), ('refunded', 'Refunded')], default='paid')),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.RichTextField(blank=True)),
                ('summary', wagtail.fields.RichTextField(blank=True)),
                ('product_rating', models.IntegerField(default=3)),
                ('price', models.IntegerField(default=300)),
                ('widgets', wagtail.fields.StreamField([('product_images', 1), ('product_options', 4), ('customer_reviews', 9)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageBlock', [], {}), 1: ('wagtail.blocks.ListBlock', (0,), {}), 2: ('wagtail.blocks.CharBlock', (), {'required': True}), 3: ('wagtail.blocks.StructBlock', [[('product_attribute_key', 2), ('product_attribute_values', 2)]], {}), 4: ('wagtail.blocks.ListBlock', (3,), {}), 5: ('wagtail.blocks.RichTextBlock', (), {'required': True}), 6: ('wagtail.blocks.IntegerBlock', (), {'required': True}), 7: ('wagtail.blocks.BooleanBlock', (), {'required': False}), 8: ('wagtail.blocks.StructBlock', [[('name', 2), ('comments', 5), ('ratting_given', 6), ('customer_verified', 7), ('customer_location', 2)]], {}), 9: ('wagtail.blocks.ListBlock', (8,), {})}, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
    ]
