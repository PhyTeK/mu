# Generated by Django 3.1.2 on 2020-12-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0019_auto_20201201_1513'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='results',
            options={'ordering': ['name', 'klasser']},
        ),
        migrations.AddField(
            model_name='results',
            name='name',
            field=models.CharField(default='Me', max_length=20),
        ),
    ]