# Generated by Django 4.1 on 2023-08-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings_dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adjustmentbalanceentry',
            options={'verbose_name_plural': 'Adjustment Balance Entries'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='earningsbalanceentry',
            options={'verbose_name_plural': 'Earnings Balance Entries'},
        ),
        migrations.AlterModelOptions(
            name='paymentbalanceentry',
            options={'verbose_name_plural': 'Payment Balance Entries'},
        ),
        migrations.AlterModelOptions(
            name='serviceentity',
            options={'verbose_name_plural': 'Service Entities'},
        ),
        migrations.AlterModelOptions(
            name='userbalanceentry',
            options={'verbose_name_plural': 'User Balance Entries'},
        ),
        migrations.AlterField(
            model_name='userbalanceaccount',
            name='payable_type',
            field=models.CharField(choices=[('RP', 'Collected Royalties Payable to Customer'), ('CP', 'Service Fees Accounts Receivable'), ('AR', 'Service Fees AR')], max_length=2),
        ),
    ]
