# Generated by Django 3.2.6 on 2021-09-29 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='stamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
