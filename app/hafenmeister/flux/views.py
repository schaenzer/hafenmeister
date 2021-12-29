import json
from json import encoder

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import FluxClusterModel, FluxWebhookTransactionModel


@method_decorator(csrf_exempt, name='dispatch')
class FluxWebhookTransactionReceiverView(View):

    def get_cluster_model(self, pk, token):
        return get_object_or_404(FluxClusterModel, pk=pk, token_str=token)

    def get(self, request, pk=None, token=None):
        self.get_cluster_model(pk=pk, token=token)
        rendered_manifests = render_to_string('flux/cluster_resource_manifests.yaml', {'inbound_url_base64': request.build_absolute_uri()})
        return HttpResponse(rendered_manifests, content_type='text/x-yaml')

    def post(self, request, pk=None, token=None):
        cluster_model = self.get_cluster_model(pk=pk, token=token)

        flux_webhook_transaction_model = FluxWebhookTransactionModel.objects.create(
            cluster = cluster_model,
            request_meta = request.META,
            request_body = json.loads(request.body)
        )

        # flux_webhook_transaction_model.queuing_for_processing()

        return HttpResponse(status=200)


flux_webhook_transaction_receiver_view = FluxWebhookTransactionReceiverView.as_view()
