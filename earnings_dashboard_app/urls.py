from django.urls import path
from . import views


urlpatterns = [
    path("index/", views.index, name="index"),
    path("earnings/", views.EarningsView.as_view(), name="earnings"),
    path("royalties/", views.RoyaltiesView.as_view(), name="royalties"),
    path("billing/", views.BillingView.as_view(), name="billing"),
    path("reports/", views.ReportsView.as_view(), name="reports"),
    path("", views.index, name="root"),
]
