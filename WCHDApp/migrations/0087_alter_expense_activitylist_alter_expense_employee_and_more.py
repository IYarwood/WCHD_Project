# Generated by Django 5.1.6 on 2025-07-07 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0086_expense_grantline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='ActivityList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.activitylist', verbose_name='Activity List'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='grantLine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.grantline', verbose_name='Grant Line'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WCHDApp.item', verbose_name='Item'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.line', verbose_name='Line'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WCHDApp.people', verbose_name='People'),
        ),
    ]
