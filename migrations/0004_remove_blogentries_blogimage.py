# Generated by Django 2.0.2 on 2018-12-10 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogentries_blogimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogentries',
            name='blogimage',
        ),
    ]