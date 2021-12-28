import secrets
import string
import uuid
import json

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class JSONEncoderNotSerializable(json.JSONEncoder):
    def default(self, o):
        return '<not serializable>'


def random_string():
    return ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(50)))


class FluxClusterModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=254, blank=True)
    token_str = models.CharField(_('token'), max_length=50, editable=False, default=random_string)


    class Meta:
        verbose_name = _("FluxClusterModel")
        verbose_name_plural = _("FluxClusterModels")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("FluxClusterModel_detail", kwargs={"pk": self.pk})



class FluxWebhookTransactionModel(models.Model):

    class STATUS(models.IntegerChoices):
        UNPROCESSED = 0, _('unprocessed')
        PROCESSED = 1, _('processed')
        ERROR = 2, _('error')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster = models.ForeignKey(FluxClusterModel, on_delete=models.CASCADE, related_name='webhook_transactions', verbose_name=_('cluster'))

    datetime_received = models.DateTimeField(_('received'), auto_now_add=True, editable=False)
    datetime_processed = models.DateTimeField(_('processed'), null=True, editable=False)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.UNPROCESSED)

    request_meta = models.JSONField(editable=False, encoder=JSONEncoderNotSerializable)
    request_body = models.JSONField(editable=False)

    class Meta:
        verbose_name = _("Webhook Transaction")
        verbose_name_plural = _("Webhook Transactions")

    def __str__(self):
        return self.id
