# Generated by Django 2.2.16 on 2023-02-23 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_auto_20230223_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(
                blank=True, upload_to='posts/', verbose_name='картинка'
            ),
        ),
    ]