from django.contrib import admin

from hafenmeister.flux.models import FluxClusterModel, FluxWebhookTransactionModel, FluxObjectModel, FluxEventModel
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
    list_filter = ['cluster', 'status', 'datetime_received']

    actions = ['process']

    @admin.action(description='Process selected Transaction')
    def process(self, request, queryset):
        del request
        for transactio in queryset:
            transactio.queuing_for_processing()


@admin.register(FluxObjectModel)
class FluxObjectAdmin(admin.ModelAdmin):
    list_display = ["id", "cluster", "object_uid", "object_namespace", "object_apiVersion", "object_kind", "object_name"]
    list_filter = ['cluster', 'object_kind', 'object_apiVersion']


@admin.register(FluxEventModel)
class FluxEventAdmin(admin.ModelAdmin):
    list_display = ["id", "object", "datetime_timestamp", "severity", "reason", "message"]
    list_filter = ['object', 'severity']
