# Generated by Django 3.1.7 on 2021-04-27 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockant_Danesh', '0005_auto_20210427_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='result_date_time',
        ),
    ]
