# Generated by Django 5.1.6 on 2025-03-04 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0010_rename_fund_line_fund_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='fund_id',
            new_name='fund',
        ),
    ]
