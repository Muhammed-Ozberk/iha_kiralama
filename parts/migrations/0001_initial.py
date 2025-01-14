# Generated by Django 5.1.4 on 2025-01-09 01:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aircrafts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in_stock', models.IntegerField(default=0)),
                ('aircraft_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='aircrafts.aircraftmodel')),
                ('part_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='parts.parttype')),
            ],
        ),
    ]
