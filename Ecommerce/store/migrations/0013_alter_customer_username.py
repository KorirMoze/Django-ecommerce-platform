# Generated by Django 4.1 on 2022-09-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
