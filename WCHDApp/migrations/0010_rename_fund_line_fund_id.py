# Generated by Django 5.1.6 on 2025-03-04 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0009_alter_fund_dept_id_alter_fund_fund_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='fund',
            new_name='fund_id',
        ),
    ]
