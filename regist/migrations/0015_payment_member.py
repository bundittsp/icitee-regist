# Generated by Django 2.1.7 on 2019-09-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regist', '0014_auto_20190909_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='member',
            field=models.BooleanField(default=False),
        ),
    ]
