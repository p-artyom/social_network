# Generated by Django 2.2.16 on 2023-03-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0007_auto_20230302_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='modified',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='modified',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]