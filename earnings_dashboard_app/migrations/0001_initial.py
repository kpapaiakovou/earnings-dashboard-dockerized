# Generated by Django 4.1 on 2023-08-06 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserBalanceAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payable_type', models.CharField(choices=[('RP', 'Collected Royalties Payable to Customer'), ('CP', 'Service Fees Accounts Receivable')], max_length=2)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='earnings_dashboard_app.currency')),
                ('service_entity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='earnings_dashboard_app.serviceentity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'service_entity', 'currency', 'payable_type')},
            },
        ),
        migrations.CreateModel(
            name='UserBalanceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('date', models.DateField()),
                ('invoice_ref', models.CharField(max_length=255)),
                ('contract_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('user_balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='earnings_dashboard_app.userbalanceaccount')),
            ],
        ),
        migrations.CreateModel(
            name='AdjustmentBalanceEntry',
            fields=[
                ('user_balance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='earnings_dashboard_app.userbalanceentry')),
                ('reason', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentBalanceEntry',
            fields=[
                ('user_balance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='earnings_dashboard_app.userbalanceentry')),
                ('entity_account_ref', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EarningsBalanceEntry',
            fields=[
                ('user_balance_entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='earnings_dashboard_app.userbalanceentry')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('incremental_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=14)),
                ('service_fee', models.DecimalField(decimal_places=2, max_digits=14)),
                ('fee_type_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='earnings_dashboard_app.product')),
            ],
        ),
    ]