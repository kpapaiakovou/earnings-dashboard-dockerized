from django.contrib import admin
from earnings_dashboard_app.models import (ServiceEntity,
                                           Currency,
                                           Product,
                                           UserBalanceAccount,
                                           UserBalanceEntry,
                                           BalanceEarningsEntryProxy,
                                           BalancePaymentEntryProxy,
                                           BalanceAdjustmentEntryProxy,
                                           BalanceEarningsEntry,
                                           BalancePaymentEntry,
                                           BalanceAdjustmentEntry,
                                           UserReport,
                                           ReportType
                                           )


# Register your models here.
@admin.register(ServiceEntity)
class ServiceEntityAdmin(admin.ModelAdmin):
    list_display = ['entity_name', 'entity_code']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(UserBalanceAccount)
class UserBalanceAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'account_type',
        'service_entity',
        'currency',
        'balance_displayed',
        'balance_reconciled',
        'balance_all_entries'
    ]


@admin.register(UserBalanceEntry)
class UserBalanceEntryAdmin(admin.ModelAdmin):
    list_display = [
        'user_balance_account',
        'get_account_type',
        'date',
        'amount',
        'entry_type',
        'entry_detail',
        'user_display_status'
    ]

    @admin.display(description='Ledger Account Type')
    def get_account_type(self, obj):
        return obj.user_balance_account.get_account_type_display()


class BalanceEarningsEntryInline(admin.StackedInline):
    model = BalanceEarningsEntry


class BalancePaymentEntryInline(admin.StackedInline):
    model = BalancePaymentEntry


class BalanceAdjustmentEntryInline(admin.StackedInline):
    model = BalanceAdjustmentEntry


@admin.register(BalanceEarningsEntryProxy)
class BalanceEarningsEntryAdmin(admin.ModelAdmin):
    list_display = [
        'user_balance_account',
        'date',
        'product',
        'total_earnings',
        'incremental_earnings',
        'service_fee',
        'currency',
        'user_display_status',
    ]
    inlines = [
        BalanceEarningsEntryInline,
    ]


@admin.register(BalancePaymentEntryProxy)
class BalancePaymentEntryAdmin(admin.ModelAdmin):
    list_display = [
        'user_balance_account',
        'get_account_type',
        'date',
        'payment_amount',
    ]
    inlines = [
        BalancePaymentEntryInline,
    ]

    @admin.display(description='Balance Account Type')
    def get_account_type(self, obj):
        return obj.user_balance_account.get_account_type_display()


@admin.register(BalanceAdjustmentEntryProxy)
class BalanceAdjustmentEntryAdmin(admin.ModelAdmin):
    list_display = [
        'user_balance_account',
        'get_account_type',
        'date',
        'get_adjustment_type_display',
        'adjustment_amount',
        'currency',
        'reason',
    ]
    inlines = [
        BalanceAdjustmentEntryInline,
    ]

    @admin.display(description='Balance Account Type')
    def get_account_type(self, obj):
        return obj.user_balance_account.get_account_type_display()

    @admin.display(description='Adjustment Type')
    def get_adjustment_type_display(self, obj):
        return obj.adjustment_type_display()


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = [
        'user_balance_account',
        'report_type',
        'name',
        'description',
        'date',
    ]
