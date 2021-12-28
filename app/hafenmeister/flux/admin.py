from django.contrib import admin

from .models import FluxClusterModel, FluxWebhookTransactionModel


@admin.register(FluxClusterModel)
class FluxClusterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "token_str"]


@admin.register(FluxWebhookTransactionModel)
class FluxWebhookTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "cluster", "datetime_received", "datetime_processed", "status", "request_meta", "request_body"]
