# Generated by Django 5.1.6 on 2025-06-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0059_remove_payperiod_id_alter_payperiod_periodid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='payroll_id',
        ),
        migrations.AddField(
            model_name='payroll',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
