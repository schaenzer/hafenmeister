from django.urls import path

from hafenmeister.sensors.views import (
    sensors_webhook_transaction_receiver_view,
)

app_name = "sensors"
urlpatterns = [
    path("<uuid:pk>/inbound/<str:token>/", view=sensors_webhook_transaction_receiver_view, name="webhook_transaction_receiver"),
]
