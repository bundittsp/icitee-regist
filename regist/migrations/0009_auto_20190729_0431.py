# Generated by Django 2.1.7 on 2019-07-29 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regist', '0008_auto_20190729_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentitem',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='regist.Article'),
        ),
    ]