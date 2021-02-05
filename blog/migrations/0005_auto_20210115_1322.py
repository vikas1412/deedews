# Generated by Django 3.1.4 on 2021-01-15 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210115_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_hindi',
            name='category',
            field=models.CharField(blank=True, choices=[('stories', 'स्टोरीज'), ('analysis', 'एनालिसिस'), ('lifestyle', 'लाइफस्टाइल'), ('other', 'अन्य')], default='अन्य', help_text='Category for article', max_length=95),
        ),
        migrations.AlterField(
            model_name='article_hindi',
            name='content',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
