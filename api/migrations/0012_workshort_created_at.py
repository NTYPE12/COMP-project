# Generated by Django 3.2.8 on 2023-03-14 23:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_einfo_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshort',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]