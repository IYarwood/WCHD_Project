# Generated by Django 5.1.6 on 2025-03-04 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0011_rename_fund_id_line_fund'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='fund',
            new_name='fund_id',
        ),
    ]
