# Generated by Django 3.1.2 on 2020-11-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0007_auto_20201106_1854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='time',
            new_name='start',
        ),
        migrations.AddField(
            model_name='student',
            name='end',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
