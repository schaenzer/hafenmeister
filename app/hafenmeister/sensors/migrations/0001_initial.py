# Generated by Django 3.2.10 on 2022-02-08 15:26

from django.db import migrations, models
import django.db.models.deletion
import hafenmeister.sensors.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorsWebhookToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token_str', models.CharField(default=hafenmeister.sensors.models.random_string, editable=False, max_length=50, verbose_name='token')),
            ],
            options={
                'verbose_name': 'Webhook Token',
                'verbose_name_plural': 'Webhook Token',
            },
        ),
        migrations.CreateModel(
            name='SensorsWebhookTransactionModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_received', models.DateTimeField(auto_now_add=True, verbose_name='received')),
                ('datetime_processed', models.DateTimeField(editable=False, null=True, verbose_name='processed')),
                ('status', models.IntegerField(choices=[(0, 'unprocessed'), (1, 'processed'), (2, 'error')], default=0)),
                ('request_meta', models.JSONField(editable=False, encoder=hafenmeister.sensors.models.JSONEncoderNotSerializable)),
                ('request_body', models.JSONField(editable=False)),
                ('token', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors_webhook_transactions', to='sensors.sensorswebhooktoken', verbose_name='token')),
            ],
            options={
                'verbose_name': 'Webhook Transaction',
                'verbose_name_plural': 'Webhook Transactions',
                'ordering': ['-datetime_received'],
            },
        ),
    ]
