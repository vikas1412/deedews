# Generated by Django 3.1.4 on 2021-01-15 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_user',
            name='sno',
        ),
        migrations.AddField(
            model_name='contact_user',
            name='id',
            field=models.AutoField(auto_created=True, default=121, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]