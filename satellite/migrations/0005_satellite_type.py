# Generated by Django 3.2.7 on 2021-12-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0004_auto_20211211_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='satellite',
            name='type',
            field=models.CharField(default='satellite', max_length=16),
        ),
    ]
