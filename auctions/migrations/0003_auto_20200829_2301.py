# Generated by Django 3.0.8 on 2020-08-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200829_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
