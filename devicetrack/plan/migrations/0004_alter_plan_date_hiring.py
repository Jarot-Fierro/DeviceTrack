# Generated by Django 5.2 on 2025-05-21 01:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_alter_plan_date_cancellation_alter_plan_date_hiring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='date_hiring',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
