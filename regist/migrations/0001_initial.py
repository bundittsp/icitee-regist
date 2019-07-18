# Generated by Django 2.1.7 on 2019-06-24 05:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price_us', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edas_id', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=150)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('page_no', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price_us', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ieee', models.CharField(blank=True, max_length=20, null=True)),
                ('is_ugm', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('method', models.CharField(choices=[('C', 'Credit Card'), ('T', 'Bank Transfer')], max_length=1)),
                ('slip', models.ImageField(blank=True, null=True, upload_to='slips/')),
                ('del_flag', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('delete_date', models.DateTimeField(auto_now=True, null=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_create_by', to=settings.AUTH_USER_MODEL)),
                ('delete_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_delete_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('currency', models.CharField(choices=[('THB', 'Thai Baht'), ('USD', 'US Dollar')], max_length=3)),
                ('add_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regist.AdditionalItem')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regist.Article')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regist.Payment')),
            ],
        ),
    ]