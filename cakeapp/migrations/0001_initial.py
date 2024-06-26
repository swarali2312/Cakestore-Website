# Generated by Django 5.0.1 on 2024-01-14 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Cake Name')),
                ('price', models.FloatField()),
                ('cat', models.IntegerField(choices=[(1, 'chocolate Cakes'), (2, 'Flavour cakes'), (3, 'Theme cakes'), (4, 'Trending cakes'), (5, 'Cupcakes')], max_length=100, verbose_name='Category')),
                ('cdetail', models.CharField(max_length=500, verbose_name='Cake Detail')),
                ('is_active', models.BooleanField(default=True)),
                ('cimage', models.ImageField(upload_to='images')),
            ],
        ),
    ]
