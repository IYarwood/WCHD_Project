# Generated by Django 5.1.6 on 2025-06-04 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0060_remove_payroll_payroll_id_payroll_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='payperiod',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.payperiod'),
            preserve_default=False,
        ),
    ]
