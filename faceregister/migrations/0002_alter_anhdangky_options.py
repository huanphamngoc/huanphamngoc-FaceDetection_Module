# Generated by Django 4.0 on 2022-01-08 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faceregister', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anhdangky',
            options={'ordering': ['sinh_vien']},
        ),
    ]