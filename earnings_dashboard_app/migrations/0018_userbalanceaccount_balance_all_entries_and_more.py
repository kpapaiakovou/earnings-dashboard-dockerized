# Generated by Django 4.1 on 2023-08-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings_dashboard_app', '0017_alter_balanceearningsentryproxy_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbalanceaccount',
            name='balance_all_entries',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14),
        ),
        migrations.AddField(
            model_name='userbalanceaccount',
            name='balance_displayed',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14),
        ),
        migrations.AddField(
            model_name='userbalanceaccount',
            name='balance_reconciled',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14),
        ),
    ]
