# Generated by Django 2.0.2 on 2018-12-10 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogentries_blogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentries',
            name='blogimage',
            field=models.ImageField(blank=True, null=True, upload_to='myimages'),
        ),
    ]
