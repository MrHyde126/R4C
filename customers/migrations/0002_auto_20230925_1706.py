# Generated by Django 3.0.9 on 2023-09-25 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('email',), 'verbose_name': 'Покупатель', 'verbose_name_plural': 'Покупатели'},
        ),
    ]