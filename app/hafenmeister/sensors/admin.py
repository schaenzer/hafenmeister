from django.contrib import admin

from hafenmeister.sensors.models import SensorsWebhookToken, SensorsWebhookTransactionModel, SensorsDevice, SensorsMeasurement
from django.utils.html import format_html

@admin.register(SensorsWebhookToken)
class FluxClusterAdmin(admin.ModelAdmin):
    list_display = ["id", "token_str"]


@admin.register(SensorsWebhookTransactionModel)
class FluxWebhookTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "token", "datetime_received", "datetime_processed", "status", "request_meta", "request_body"]
    list_filter = ['token', 'status', 'datetime_received']

    actions = ['process']

    @admin.action(description='Process selected Transaction')
    def process(self, request, queryset):
        del request
        for transaction in queryset:
            transaction.queuing_for_processing()


@admin.register(SensorsDevice)
class SensorsDeviceAdmin(admin.ModelAdmin):
    list_display = ["id", "device_id"]

@admin.register(SensorsMeasurement)
class SensorsMeasurementAdmin(admin.ModelAdmin):
    list_display = ["id", "device", "timestemp", "temperature", "humidity", "battery"]
    list_filter = ['device', 'timestemp']
