# Generated by Django 3.2.8 on 2023-03-14 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_job_job_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
