from django.urls import path

from .views import (
    flux_webhook_transaction_receiver_view,
)

app_name = "flux"
urlpatterns = [
    path("cluster/<uuid:pk>/inbound/<str:token>/", view=flux_webhook_transaction_receiver_view, name="webhook_transaction_receiver"),
]
