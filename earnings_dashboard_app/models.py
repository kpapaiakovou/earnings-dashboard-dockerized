from django.db import models
from django.contrib.auth.models import User


class ServiceEntity(models.Model):
    entity_name = models.CharField(max_length=255)
    entity_code = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "Service Entities"

    def __str__(self):
        return str(self.entity_name)


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return "%s - %s" % (self.code, self.name)


class Product(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.code, self.name)


class UserBalanceAccount(models.Model):

    class Meta:
        unique_together = ('user', 'service_entity', 'currency', 'account_type')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_entity = models.ForeignKey(ServiceEntity, on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    account_type = models.CharField(
        max_length=2,
        choices=[
            ('AR', 'Accounts Receivable'),
            ('RP', 'Royalties Payable')
        ]
    )

    def __str__(self):
        return "%s-%s-%s|%s|%s" % (
            self.service_entity.entity_code,
            self.account_type,
            str(self.currency.code),
            str(self.id),
            str(self.user.username),
        )

    def balance_displayed(self):
        queryset = self.userbalanceentry_set.all().filter(user_display_status="VS")
        return queryset.aggregate(models.Sum('amount'))['amount__sum']

    def balance_reconciled(self):
        queryset = self.userbalanceentry_set.all().exclude(user_display_status="PN")
        return queryset.aggregate(models.Sum('amount'))['amount__sum']

    def balance_all_entries(self):
        queryset = self.userbalanceentry_set.all()
        return queryset.aggregate(models.Sum('amount'))['amount__sum']


class UserBalanceEntry(models.Model):
    user_balance_account = models.ForeignKey(
        UserBalanceAccount,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=0)
    date = models.DateField()
    invoice_ref = models.CharField(null=True, blank=True, max_length=255)
    contract_ref = models.CharField(null=True, blank=True, max_length=255)
    entry_type = models.CharField(
        max_length=3,
        choices=[
            ("ARS", "Billed Service Fee"),
            ("ARP", "Service Fee Payment"),
            ("ARI", "AR Balance Adjustment Increase"),
            ("ARD", "AR Balance Adjustment Decrease"),
            ("RPE", "Net Royalties Payable"),
            ("RPP", "Net Royalty Payment"),
            ("RPI", "RP Balance Adjustment Increase"),
            ("RPD", "RP Balance Adjustment Decrease")
        ],
        editable=False
    )
    entry_detail = models.CharField(max_length=255, null=True, blank=True, editable=False)
    user_display_status = models.CharField(
        max_length=2,
        choices=[
            ("PN", "PENDING - NOT RECONCILED"),
            ("PR", "PENDING - RECONCILED"),
            ("VS", "VISIBLE"),
        ],
        default="PN"
    )

    class Meta:
        verbose_name_plural = "User Balance Ledger"

    def save(self, *args, **kwargs):
        if hasattr(self, 'balanceearningsentry'):
            self.entry_detail = self.balanceearningsentry.product.name
            if self.user_balance_account.account_type == "AR":
                self.entry_type = "ARS"
                self.amount = abs(self.balanceearningsentry.service_fee)
            elif self.user_balance_account.account_type == "RP":
                self.entry_type = "RPE"
                self.amount = (abs(self.balanceearningsentry.total_earnings) -
                                       abs(self.balanceearningsentry.service_fee))
        elif hasattr(self, 'balancepaymententry'):
            if self.user_balance_account.account_type == "AR":
                self.entry_type = "ARP"
                self.entry_detail = "Payment Received - Thank you"
            elif self.user_balance_account.account_type == "RP":
                self.entry_type = "RPP"
                self.entry_detail = "Payment Sent from Royalty Balance"
            self.amount = -abs(self.balancepaymententry.payment_amount)
        elif hasattr(self, 'balanceadjustmententry'):
            self.entry_detail = self.balanceadjustmententry.reason
            if self.balanceadjustmententry.adjustment_type == "INC":
                if self.user_balance_account.account_type == "AR":
                    self.entry_type = "ARI"
                elif self.user_balance_account.account_type == "RP":
                    self.entry_type = "RPI"
                self.amount = abs(self.balanceadjustmententry.adjustment_amount)
            elif self.balanceadjustmententry.adjustment_type == "DEC":
                if self.user_balance_account.account_type == "AR":
                    self.entry_type = "ARD"
                elif self.user_balance_account.account_type == "RP":
                    self.entry_type = "RPD"
                self.amount = -abs(self.balanceadjustmententry.adjustment_amount)
        super(UserBalanceEntry, self).save(*args, **kwargs)


class BalanceEarningsEntryProxyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(balanceearningsentry__isnull=True)


class BalanceEarningsEntryProxy(UserBalanceEntry):

    objects = BalanceEarningsEntryProxyManager()

    class Meta:
        proxy = True
        verbose_name = "Balance Earnings Entry"
        verbose_name_plural = "Balance Earnings Entries"

    def product(self):
        return self.balanceearningsentry.product

    def total_earnings(self):
        return self.balanceearningsentry.total_earnings

    def incremental_earnings(self):
        return self.balanceearningsentry.incremental_earnings

    def service_fee(self):
        return self.balanceearningsentry.service_fee

    def currency(self):
        return self.user_balance_account.currency.code


class BalancePaymentEntryProxyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(balancepaymententry__isnull=True)


class BalancePaymentEntryProxy(UserBalanceEntry):
    objects = BalancePaymentEntryProxyManager()

    class Meta:
        proxy = True
        verbose_name = "Balance Payment Entry"
        verbose_name_plural = "Balance Payment Entries"

    def currency(self):
        return self.user_balance_account.currency.code

    def payment_amount(self):
        return self.balancepaymententry.payment_amount


class BalanceAdjustmentEntryProxyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(balanceadjustmententry__isnull=True)


class BalanceAdjustmentEntryProxy(UserBalanceEntry):
    objects = BalanceAdjustmentEntryProxyManager()

    class Meta:
        proxy = True
        verbose_name = "Balance Adjustment Entry"
        verbose_name_plural = "Balance Adjustment Entries"

    def adjustment_type(self):
        return self.balanceadjustmententry.adjustment_type

    def adjustment_type_display(self):
        return self.balanceadjustmententry.get_adjustment_type_display()

    def reason(self):
        return self.balanceadjustmententry.reason

    def currency(self):
        return self.user_balance_account.currency.code

    def adjustment_amount(self):
        return self.balanceadjustmententry.adjustment_amount


class BalanceEarningsEntry(models.Model):
    balance_entry = models.OneToOneField(UserBalanceEntry, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    total_earnings = models.DecimalField(max_digits=14, decimal_places=2)
    incremental_earnings = models.DecimalField(max_digits=14, decimal_places=2, blank=True)
    service_fee = models.DecimalField(max_digits=14, decimal_places=2)
    fee_type_ref = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        verbose_name_plural = "Balance Earnings Entries"

    def save(self, *args, **kwargs):
        self.total_earnings = abs(self.total_earnings)
        self.incremental_earnings = abs(self.incremental_earnings)
        self.service_fee = abs(self.service_fee)
        if self.balance_entry.user_balance_account.account_type == "AR":
            self.balance_entry.amount = self.service_fee
        elif self.balance_entry.user_balance_account.account_type == "RP":
            self.balance_entry.amount = self.total_earnings - self.service_fee
        self.balance_entry.save()
        super(BalanceEarningsEntry, self).save(*args, **kwargs)


class BalancePaymentEntry(models.Model):
    balance_entry = models.OneToOneField(
        UserBalanceEntry,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    payment_amount = models.DecimalField(max_digits=14, decimal_places=2)
    bank_custom_name = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        verbose_name_plural = "Balance Payment Entries"

    def save(self, *args, **kwargs):
        self.payment_amount = abs(self.payment_amount)
        self.balance_entry.amount = -abs(self.payment_amount)
        self.balance_entry.save()
        super(BalancePaymentEntry, self).save(*args, **kwargs)


class BalanceAdjustmentEntry(models.Model):
    balance_entry = models.OneToOneField(
        UserBalanceEntry,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    adjustment_amount = models.DecimalField(max_digits=14, decimal_places=2)
    adjustment_type = models.CharField(
        max_length=3,
        choices=[
            ("INC", "Balance Increase"),
            ("DEC", "Balance Decrease")
        ]
    )
    reason = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Balance Adjustment Entries"

    def save(self, *args, **kwargs):
        self.adjustment_amount = abs(self.adjustment_amount)
        if self.adjustment_type == "DEC":
            self.balance_entry.amount = -abs(self.adjustment_amount)
        elif self.adjustment_type == "INC":
            self.balance_entry.amount = abs(self.adjustment_amount)
        self.balance_entry.save()
        super(BalanceAdjustmentEntry, self).save(*args, **kwargs)


class ReportType(models.Model):
    name = models.CharField(max_length=255)
    filetype = models.CharField(max_length=4)

    class Meta:
        verbose_name = "User Report Type"
        verbose_name_plural = "User Report Types"

    def __str__(self):
        return "%s_%s" % (self.name, self.filetype)


class UserReport(models.Model):
    user_balance_account = models.ForeignKey(
        UserBalanceAccount,
        on_delete=models.CASCADE,
    )
    report_type = models.ForeignKey(
        ReportType,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_report_files/')

    class Meta:
        verbose_name = "User Report"
        verbose_name_plural = "User Reports"

    def __str__(self):
        return "%s-%s" % (self.name, str(self.report_type))
