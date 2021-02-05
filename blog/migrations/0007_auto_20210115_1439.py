# Generated by Django 3.1.4 on 2021-01-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210115_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_hindi',
            name='category_english',
            field=models.CharField(blank=True, choices=[('stories', 'stories'), ('analysis', 'analysis'), ('lifestyle', 'lifestyle'), ('other', 'other')], default='अन्य', help_text='Category for article', max_length=95),
        ),
        migrations.AlterField(
            model_name='article_hindi',
            name='category',
            field=models.CharField(blank=True, choices=[('stories', 'स्टोरीज'), ('analysis', 'एनालिसिस'), ('lifestyle', 'लाइफस्टाइल'), ('other', 'अन्य')], default='अन्य', help_text='Category for article', max_length=95),
        ),
    ]