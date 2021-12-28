# Generated by Django 3.2.10 on 2021-12-28 11:23

from django.db import migrations, models
import hafenmeister.flux.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FluxClusterModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=254, verbose_name='name')),
                ('token_str', models.CharField(default=hafenmeister.flux.models.random_string, editable=False, max_length=50, verbose_name='token')),
            ],
            options={
                'verbose_name': 'FluxClusterModel',
                'verbose_name_plural': 'FluxClusterModels',
            },
        ),
    ]
