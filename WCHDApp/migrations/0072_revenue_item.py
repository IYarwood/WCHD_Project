# Generated by Django 5.1.6 on 2025-06-18 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0071_alter_expense_warrant'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenue',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='WCHDApp.item'),
            preserve_default=False,
        ),
    ]
