# Generated by Django 3.1.2 on 2020-11-27 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0013_auto_20201127_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multi',
            name='date',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='multi',
            name='end',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='multi',
            name='start',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='multi',
            name='tid',
            field=models.CharField(max_length=20, null=True),
        ),
    ]