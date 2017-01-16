# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 03:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20170109_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id_category',
            field=models.ForeignKey(blank=True, db_column='id_category', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='user.Category'),
        ),
        migrations.AlterField(
            model_name='card',
            name='id_theme',
            field=models.ForeignKey(db_column='id_theme', on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='user.Theme'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id_theme',
            field=models.ForeignKey(db_column='id_theme', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='user.Theme'),
        ),
    ]