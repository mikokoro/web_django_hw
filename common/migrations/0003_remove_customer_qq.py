# Generated by Django 3.1.3 on 2020-11-26 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_customer_qq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='qq',
        ),
    ]
