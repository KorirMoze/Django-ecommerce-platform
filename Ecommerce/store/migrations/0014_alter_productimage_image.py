# Generated by Django 4.1 on 2022-10-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
    ]
