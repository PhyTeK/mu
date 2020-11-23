# Generated by Django 3.1.2 on 2020-11-08 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0008_auto_20201108_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AddField(
            model_name='student',
            name='klass',
            field=models.CharField(default='4a', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='studid',
            field=models.IntegerField(blank=True, default=1002, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
