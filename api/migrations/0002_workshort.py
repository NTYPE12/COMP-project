# Generated by Django 3.2.8 on 2023-03-14 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkShort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('job_title', models.CharField(max_length=255, null=True)),
                ('specialisms', models.CharField(max_length=255, null=True)),
                ('min_sallery', models.CharField(max_length=255, null=True)),
                ('overview', models.TextField(null=True)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('website', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('experience', models.CharField(max_length=255, null=True)),
                ('age', models.CharField(max_length=255, null=True)),
                ('current_salary', models.CharField(max_length=255, null=True)),
                ('expected_salary', models.CharField(max_length=255, null=True)),
                ('languages', models.CharField(max_length=255, null=True)),
                ('education', models.CharField(max_length=255, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo')),
            ],
        ),
    ]
