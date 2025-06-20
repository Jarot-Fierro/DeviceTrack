# Generated by Django 5.2 on 2025-06-04 22:06

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0005_rename_new_data_brandhistory_data_and_more'),
        ('device_owner', '0002_rename_new_data_deviceownerhistory_data_and_more'),
        ('inks', '0001_initial'),
        ('model', '0002_rename_new_data_modelhistory_data_and_more'),
        ('subcategory', '0002_rename_new_data_subcategoryhistory_data_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id_printer', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('number_serie', models.CharField(max_length=100)),
                ('hh', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='ACTIVE', max_length=150)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('device_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device_owner.deviceowner')),
                ('inks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inks.inks')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.model')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcategory.subcategory')),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrinterHistory',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id_printer_history', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('id_printer', models.CharField(max_length=200)),
                ('operation', models.CharField(max_length=100)),
                ('data', models.JSONField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_login_history', models.CharField(max_length=100)),
                ('user_login', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
    ]
