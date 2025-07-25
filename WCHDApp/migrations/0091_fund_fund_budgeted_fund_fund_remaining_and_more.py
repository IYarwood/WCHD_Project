# Generated by Django 5.1.6 on 2025-07-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0090_remove_line_line_encumbered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='fund_budgeted',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Budgeted'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fund',
            name='fund_remaining',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Remaining'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fund',
            name='fund_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Total Given'),
            preserve_default=False,
        ),
    ]
