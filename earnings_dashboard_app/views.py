from django.shortcuts import redirect, reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from earnings_dashboard_app.models import (
    BalanceEarningsEntry, UserBalanceEntry, UserReport, UserBalanceAccount)


def index(request):
    return redirect(reverse("earnings"))


class EarningsView(LoginRequiredMixin,ListView):
    login_url = "/accounts/login"
    redirect_field_name = "redirect_to"
    model = BalanceEarningsEntry
    template_name = "earnings_dashboard_app/earnings.html"
    context_object_name = "earnings_entries"
    paginate_by = 20

    def get_queryset(self):
        queryset = BalanceEarningsEntry.objects.filter(
            balance_entry__user_balance_account__user=self.request.user,
            balance_entry__user_display_status="VS"
        ).order_by("-balance_entry__date")
        return queryset


class RoyaltiesView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    redirect_field_name = "redirect_to"
    model = UserBalanceEntry
    template_name = "earnings_dashboard_app/royalties.html"
    context_object_name = "royalty_balance_entries"
    paginate_by = 20
    user_balance_account = None

    def get_user_balance_account(self):
        if not self.user_balance_account:
            account_id = self.request.GET.get('account')
            if account_id:
                self.user_balance_account = UserBalanceAccount.objects.filter(
                    user=self.request.user,
                    account_type="RP",
                    account_id=account_id,
                )
            else:
                self.user_balance_account = UserBalanceAccount.objects.filter(
                    user=self.request.user,
                    account_type="RP"
                ).first()
        return self.user_balance_account

    def get_queryset(self):
        queryset = UserBalanceEntry.objects.filter(
            user_balance_account=self.get_user_balance_account(),
            user_display_status='VS',
        ).order_by("-date")
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        if self.user_balance_account is not None:
            context["current_balance"] = self.user_balance_account.balance_displayed()
        else:
            context["current_balance"] = 0.00
        return context


class BillingView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    redirect_field_name = "redirect_to"
    model = UserBalanceEntry
    template_name = "earnings_dashboard_app/billing.html"
    context_object_name = "billing_balance_entries"
    paginate_by = 20
    user_balance_account = None

    def get_user_balance_account(self):
        if not self.user_balance_account:
            account_id = self.request.GET.get('account')
            if account_id:
                self.user_balance_account = UserBalanceAccount.objects.filter(
                    user=self.request.user,
                    account_type="AP",
                    account_id=account_id,
                )
            else:
                self.user_balance_account = UserBalanceAccount.objects.filter(
                    user=self.request.user,
                    account_type="AR"
                ).first()
        return self.user_balance_account

    def get_queryset(self):
        queryset = UserBalanceEntry.objects.filter(
            user_balance_account=self.get_user_balance_account(),
            user_display_status='VS',
        ).order_by("-date")
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        if self.user_balance_account is not None:
            context["current_balance"] = self.user_balance_account.balance_displayed()
        else:
            context["current_balance"] = 0.00
        return context


class ReportsView(LoginRequiredMixin,ListView):
    login_url = "/accounts/login"
    redirect_field_name = "redirect_to"
    template_name = "earnings_dashboard_app/reports.html"
    model = UserReport
    context_object_name = "user_reports"
    paginate_by = 20

    def get_queryset(self):
        queryset = UserReport.objects.filter(
            user_balance_account__user=self.request.user,
        ).order_by("-date")
        return queryset
