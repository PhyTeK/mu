# Generated by Django 3.1.2 on 2020-11-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mu', '0014_remove_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='week',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
