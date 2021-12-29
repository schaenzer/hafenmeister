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


class FluxClusterModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=254)
    token_str = models.CharField(_('token'), max_length=50, editable=False, default=random_string)


    class Meta:
        verbose_name = _("Cluster")
        verbose_name_plural = _("Clusters")

    def __str__(self):
        return self.name

    def get_inbound_url(self):
        return reverse("flux:webhook_transaction_receiver", kwargs={'pk': self.pk, 'token': self.token_str})

    # def get_absolute_url(self):
    #     return reverse("FluxClusterModel_detail", kwargs={"pk": self.pk})


class FluxObjectNamespaceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster = models.ForeignKey(FluxClusterModel, on_delete=models.CASCADE, related_name='object_namespaces', verbose_name=_('cluster'))
    name = models.CharField(_('name'), max_length=254)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('cluster', 'name',)


class FluxObjectKindModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster = models.ForeignKey(FluxClusterModel, on_delete=models.CASCADE, related_name='object_kinds', verbose_name=_('cluster'))
    name = models.CharField(_('name'), max_length=254)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('cluster', 'name',)


class FluxObjectApiVersionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster = models.ForeignKey(FluxClusterModel, on_delete=models.CASCADE, related_name='object_api_versions', verbose_name=_('cluster'))
    name = models.CharField(_('name'), max_length=254)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('cluster', 'name',)


class FluxObjectModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cluster = models.ForeignKey(FluxClusterModel, on_delete=models.CASCADE, related_name='flux_objects', verbose_name=_('cluster'))
    object_uid = models.UUIDField(_('uid'))
    object_kind = models.ForeignKey(FluxObjectKindModel, on_delete=models.CASCADE, related_name='flux_objects', verbose_name=_('kind'))
    object_name = models.CharField(_('name'), max_length=254)
    object_namespace = models.ForeignKey(FluxObjectNamespaceModel, on_delete=models.CASCADE, related_name='flux_objects', verbose_name=_('namespace'))
    object_apiVersion = models.ForeignKey(FluxObjectApiVersionModel, on_delete=models.CASCADE, related_name='flux_objects', verbose_name=_('api version'))

    class Meta:
        verbose_name = _("Object")
        verbose_name_plural = _("Objects")
        unique_together = ('cluster', 'object_uid',)

    def __str__(self):
        return f'{self.cluster}/{self.object_namespace}/{self.object_name}'

class FluxEventModel(models.Model):
    class SEVERITY(models.TextChoices):
        INFO = 'info', _('info')
        ERROR = 'error', _('error')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object = models.ForeignKey(FluxObjectModel, on_delete=models.CASCADE, related_name='events', verbose_name=_('object'))
    reason = models.CharField(_('reason'), max_length=254)
    message = models.TextField(_('message'))
    severity = models.CharField(_('severity'), max_length=10, choices=SEVERITY.choices)
    datetime_timestamp = models.DateTimeField(_('timestamp'))

    associated_transaction = models.OneToOneField('flux.FluxWebhookTransactionModel', on_delete=models.SET_NULL, null=True,  editable=False)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['-datetime_timestamp',]

    def __str__(self):
        return str(self.pk)


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
        ordering = ['-datetime_received',]

    def __str__(self):
        return str(self.pk)

    def queuing_for_processing(self):
        queuing_for_processing.send(sender=self.__class__, instance=self)

    @transaction.atomic
    def process(self):
        flux_object_kind_model, created = FluxObjectKindModel.objects.get_or_create(
            cluster=self.cluster,
            name=self.request_body['involvedObject']['kind']
        )

        flux_object_namespace_model, created = FluxObjectNamespaceModel.objects.get_or_create(
            cluster=self.cluster,
            name=self.request_body['involvedObject']['namespace']
        )

        flux_object_api_version_model, created = FluxObjectApiVersionModel.objects.get_or_create(
            cluster=self.cluster,
            name=self.request_body['involvedObject']['apiVersion']
        )

        flux_object_model, created = FluxObjectModel.objects.update_or_create(
            cluster=self.cluster, object_uid=self.request_body['involvedObject']['uid'],
            defaults={
                'object_kind': flux_object_kind_model,
                'object_name': self.request_body['involvedObject']['name'],
                'object_namespace': flux_object_namespace_model,
                'object_apiVersion': flux_object_api_version_model,
            },
        )

        FluxEventModel.objects.update_or_create(
            associated_transaction=self,
            defaults= {
                'object': flux_object_model,
                'reason': self.request_body['reason'],
                'message': self.request_body['message'],
                'severity': self.request_body['severity'],
                'datetime_timestamp': self.request_body['timestamp']
            }
        )

        self.status = self.STATUS.PROCESSED
        self.datetime_processed = timezone.now()
        self.save(update_fields=['status', 'datetime_processed'])
