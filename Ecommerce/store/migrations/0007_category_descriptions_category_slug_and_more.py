# Generated by Django 4.1 on 2022-09-10 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_category_status_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descriptions',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='descriptions',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=200, null=True),
        ),
    ]