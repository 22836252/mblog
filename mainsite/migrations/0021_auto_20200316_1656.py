# Generated by Django 3.0.3 on 2020-03-16 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0020_products_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='href',
            field=models.CharField(default='nourl', max_length=200),
        ),
        migrations.AddField(
            model_name='products',
            name='imagelink',
            field=models.CharField(default='nourl', max_length=200),
        ),
    ]