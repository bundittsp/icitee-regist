# Generated by Django 2.1.7 on 2019-09-09 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regist', '0012_auto_20190908_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalitem',
            name='early_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='additionalitem',
            name='early_price_us',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
