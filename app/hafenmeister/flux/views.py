import json
from json import encoder

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import FluxClusterModel, FluxWebhookTransactionModel


@method_decorator(csrf_exempt, name='dispatch')
class FluxWebhookTransactionReceiverView(View):

    def post(self, request, pk=None, token=None):
        cluster_model = get_object_or_404(FluxClusterModel, pk=pk, token_str=token)


        FluxWebhookTransactionModel.objects.create(
            cluster = cluster_model,
            request_meta = request.META,
            request_body = json.loads(request.body)
        )

        return HttpResponse(status=200)


flux_webhook_transaction_receiver_view = FluxWebhookTransactionReceiverView.as_view()
