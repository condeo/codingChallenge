# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-26 22:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarRepair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropoff_date', models.DateField(default=datetime.date.today)),
                ('pickup_date', models.DateField(blank=True, null=True)),
                ('type_of_repair', models.CharField(choices=[('A', 'oil change'), ('B', 'tire repair'), ('C', 'engine inspection'), ('D', 'tune-up'), ('E', 'brake service'), ('F', 'oil gasket replacement')], max_length=1, null=True)),
            ],
            options={
                'ordering': ['-dropoff_date'],
                'db_table': 'shop_workflow_fact',
                'verbose_name': 'repair',
                'verbose_name_plural': 'repairs',
            },
        ),
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-name'],
                'verbose_name': 'Mechanic',
                'verbose_name_plural': 'Mechanics',
            },
        ),
        migrations.AddField(
            model_name='carrepair',
            name='assigned_mechanic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_repairs', to='shop_workflow.Mechanic'),
        ),
    ]
