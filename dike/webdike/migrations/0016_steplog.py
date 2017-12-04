# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webdike', '0015_document_last_valid_step_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('vote', models.IntegerField()),
                ('population', models.FloatField()),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webdike.Step')),
            ],
        ),
    ]