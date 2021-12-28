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
    name = models.CharField(_('name'), max_length=254)
    token_str = models.CharField(_('token'), max_length=50, editable=False, default=random_string)


    class Meta:
        verbose_name = _("FluxClusterModel")
        verbose_name_plural = _("FluxClusterModels")

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
        unique_together = ('cluster', 'object_uid',)


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

        # print(self.request_body['reason'])
        # print(self.request_body['message'])
        # print(self.request_body['severity'])
        # print(self.request_body['timestamp'])
