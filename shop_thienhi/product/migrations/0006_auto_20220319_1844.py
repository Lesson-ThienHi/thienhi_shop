# Generated by Django 3.2.12 on 2022-03-19 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20220319_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='timestamp',
            field=models.FloatField(null=True),
        ),
    ]
