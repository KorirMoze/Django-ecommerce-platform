# Generated by Django 4.1 on 2022-10-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_rename_products_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
