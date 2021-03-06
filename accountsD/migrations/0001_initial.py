# Generated by Django 3.1.4 on 2021-01-11 13:02

import accountsD.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('fullname', models.CharField(max_length=213)),
                ('username', models.CharField(max_length=60)),
                ('profile_photo', models.ImageField(default='profile/default.png', upload_to=accountsD.models.user_directory_path)),
                ('dob', models.CharField(blank=True, max_length=213, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Custom', 'Custom')], max_length=15, null=True)),
                ('number', models.CharField(blank=True, default='', max_length=213, null=True)),
                ('bio', models.TextField(blank=True, default='', max_length=513, null=True)),
            ],
        ),
    ]
