# Generated by Django 4.1 on 2022-09-10 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category_product_trending_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.BooleanField(default=False, help_text='0=default, 1=Hidden'),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=False, help_text='0=default, 1=Hidden'),
        ),
    ]
