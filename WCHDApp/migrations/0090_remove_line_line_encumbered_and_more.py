# Generated by Django 5.1.6 on 2025-07-08 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0089_grantline_line_budget_remaining'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='line_encumbered',
        ),
        migrations.AddField(
            model_name='line',
            name='line_budget_remaining',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Budget Remaining'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='line_item',
            field=models.CharField(max_length=255, verbose_name='Line Item'),
        ),
        migrations.AlterField(
            model_name='line',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WCHDApp.dept', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='line',
            name='fund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WCHDApp.fund', verbose_name='Fund'),
        ),
    ]
