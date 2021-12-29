
from config import celery_app
from hafenmeister.flux.models import FluxWebhookTransactionModel
from hafenmeister.flux.signals import queuing_for_processing
from django.dispatch import receiver
from django.db import transaction


@celery_app.task()
def flux_processing_webhook_transaction(pk):
    flux_webhook_transaction_model = FluxWebhookTransactionModel.objects.get(pk=pk)

    try:
        flux_webhook_transaction_model.process()

    except Exception as e:
        flux_webhook_transaction_model.status = FluxWebhookTransactionModel.STATUS.ERROR
        flux_webhook_transaction_model.save(update_fields=['status',])
        raise e

@receiver(queuing_for_processing, sender=FluxWebhookTransactionModel)
def queuing_webhook_transaction_for_processing(sender, instance, *args, **kwargs):
    print(instance)
    transaction.on_commit(lambda: flux_processing_webhook_transaction.delay(instance.pk))
