from django.contrib import admin

from .models import FluxClusterModel, FluxWebhookTransactionModel
from django.utils.html import format_html

@admin.register(FluxClusterModel)
class FluxClusterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "token_str", "cluster_actions"]

    def cluster_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Inbound URL</a>&nbsp;',

            obj.get_inbound_url(),
        )
    cluster_actions.short_description = 'Account Actions'
    cluster_actions.allow_tags = True


@admin.register(FluxWebhookTransactionModel)
class FluxWebhookTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "cluster", "datetime_received", "datetime_processed", "status", "request_meta", "request_body"]
