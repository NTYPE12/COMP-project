# Generated by Django 3.2.8 on 2023-03-14 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_admininfo_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='einfo',
            name='ountry',
            field=models.CharField(max_length=255, null=True),
        ),
    ]