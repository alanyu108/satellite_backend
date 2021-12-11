# Generated by Django 3.2.7 on 2021-11-07 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0002_auto_20211007_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='satellite',
            name='country',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='satellite',
            name='launch_date',
            field=models.CharField(default='0000-00-00', max_length=10),
        ),
        migrations.AddField(
            model_name='satellite',
            name='launch_site',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='satellite',
            name='object_status',
            field=models.CharField(default='Operational', max_length=32),
        ),
    ]