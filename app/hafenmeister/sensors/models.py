import json
import secrets
import string
import uuid

from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from hafenmeister.flux.signals import queuing_for_processing

class JSONEncoderNotSerializable(json.JSONEncoder):
    def default(self, o):
        return '<not serializable>'


def random_string():
    return ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(50)))


class SensorsWebhookToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_str = models.CharField(_('token'), max_length=50, editable=False, default=random_string)


    class Meta:
        verbose_name = _("Webhook Token")
        verbose_name_plural = _("Webhook Token")

    def __str__(self):
        return str(self.id)

    def get_inbound_url(self):
        return reverse("sensors:webhook_transaction_receiver", kwargs={'pk': self.pk, 'token': self.token_str})



class SensorsWebhookTransactionModel(models.Model):

    class STATUS(models.IntegerChoices):
        UNPROCESSED = 0, _('unprocessed')
        PROCESSED = 1, _('processed')
        ERROR = 2, _('error')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(SensorsWebhookToken, null=True, on_delete=models.SET_NULL, related_name='sensors_webhook_transactions', verbose_name=_('token'))

    datetime_received = models.DateTimeField(_('received'), auto_now_add=True, editable=False)
    datetime_processed = models.DateTimeField(_('processed'), null=True, editable=False)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.UNPROCESSED)

    request_meta = models.JSONField(editable=False, encoder=JSONEncoderNotSerializable)
    request_body = models.JSONField(editable=False)

    class Meta:
        verbose_name = _("Webhook Transaction")
        verbose_name_plural = _("Webhook Transactions")
        ordering = ['-datetime_received',]

    def __str__(self):
        return str(self.pk)

    def queuing_for_processing(self):
        queuing_for_processing.send(sender=self.__class__, instance=self)

    @transaction.atomic
    def process(self):
        pass
