import json
from json import encoder

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from hafenmeister.sensors.models import (
    SensorsWebhookToken,
    SensorsWebhookTransactionModel,
)


@method_decorator(csrf_exempt, name='dispatch')
class SensorsWebhookTransactionReceiverView(View):

    def get_token_model(self, pk, token):
        return get_object_or_404(SensorsWebhookToken, pk=pk, token_str=token)

    def post(self, request, pk=None, token=None):
        token_model = self.get_token_model(pk=pk, token=token)

        flux_webhook_transaction_model = SensorsWebhookTransactionModel.objects.create(
            token = token_model,
            request_meta = request.META,
            request_body = json.loads(request.body)
        )

        flux_webhook_transaction_model.queuing_for_processing()

        return HttpResponse(status=200)

sensors_webhook_transaction_receiver_view = SensorsWebhookTransactionReceiverView.as_view()
