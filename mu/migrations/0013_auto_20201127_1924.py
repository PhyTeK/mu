# Generated by Django 3.1.2 on 2020-11-27 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0012_auto_20201127_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multi',
            name='date',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='multi',
            name='tid',
            field=models.CharField(max_length=10, null=True),
        ),
    ]