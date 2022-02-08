
from config import celery_app
from hafenmeister.sensors.models import SensorsWebhookTransactionModel
from hafenmeister.sensors.signals import queuing_for_processing
from django.dispatch import receiver
from django.db import transaction


@celery_app.task()
def flux_processing_webhook_transaction(pk):
    flux_webhook_transaction_model = SensorsWebhookTransactionModel.objects.get(pk=pk)

    try:
        flux_webhook_transaction_model.process()

    except Exception as e:
        flux_webhook_transaction_model.status = SensorsWebhookTransactionModel.STATUS.ERROR
        flux_webhook_transaction_model.save(update_fields=['status',])
        raise e

@receiver(queuing_for_processing, sender=SensorsWebhookTransactionModel)
def queuing_webhook_transaction_for_processing(sender, instance, *args, **kwargs):
    del sender, args, kwargs
    transaction.on_commit(lambda: flux_processing_webhook_transaction.delay(instance.pk))
