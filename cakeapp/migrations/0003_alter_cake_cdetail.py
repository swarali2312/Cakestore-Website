# Generated by Django 5.0.1 on 2024-01-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeapp', '0002_alter_cake_cimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='cdetail',
            field=models.TextField(verbose_name='Cake Detail'),
        ),
    ]
