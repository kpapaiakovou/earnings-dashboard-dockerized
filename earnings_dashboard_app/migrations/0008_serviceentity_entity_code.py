# Generated by Django 4.1 on 2023-08-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earnings_dashboard_app', '0007_balanceadjustmententry_balanceearningsentry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceentity',
            name='entity_code',
            field=models.CharField(default='HLT', max_length=3),
            preserve_default=False,
        ),
    ]
