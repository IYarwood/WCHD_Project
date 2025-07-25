# Generated by Django 5.1.6 on 2025-03-25 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WCHDApp', '0019_rename_vendor_customer_invoice_people_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='business',
            new_name='people',
        ),
        migrations.RenameField(
            model_name='voucher',
            old_name='vendor',
            new_name='people',
        ),
        migrations.AlterField(
            model_name='people',
            name='name_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Customer/Vendor'),
        ),
    ]
