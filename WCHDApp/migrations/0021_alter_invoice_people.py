# Generated by Django 5.1.6 on 2025-03-25 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0020_rename_business_purchaseorder_people_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WCHDApp.people', verbose_name='TESTING'),
        ),
    ]
