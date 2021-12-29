# Generated by Django 3.2.10 on 2021-12-28 17:02

from django.db import migrations, models
import django.db.models.deletion
import hafenmeister.flux.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flux', '0002_fluxwebhooktransactionmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluxclustermodel',
            name='name',
            field=models.CharField(max_length=254, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='fluxwebhooktransactionmodel',
            name='request_meta',
            field=models.JSONField(editable=False, encoder=hafenmeister.flux.models.JSONEncoderNotSerializable),
        ),
        migrations.CreateModel(
            name='FluxObjectNamespaceModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254, verbose_name='name')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_namespaces', to='flux.fluxclustermodel', verbose_name='cluster')),
            ],
            options={
                'unique_together': {('cluster', 'name')},
            },
        ),
        migrations.CreateModel(
            name='FluxObjectKindModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254, verbose_name='name')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_kinds', to='flux.fluxclustermodel', verbose_name='cluster')),
            ],
            options={
                'unique_together': {('cluster', 'name')},
            },
        ),
        migrations.CreateModel(
            name='FluxObjectApiVersionModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254, verbose_name='name')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_api_versions', to='flux.fluxclustermodel', verbose_name='cluster')),
            ],
            options={
                'unique_together': {('cluster', 'name')},
            },
        ),
        migrations.CreateModel(
            name='FluxObjectModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_uid', models.UUIDField(verbose_name='uid')),
                ('object_name', models.CharField(max_length=254, verbose_name='name')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='flux.fluxclustermodel', verbose_name='cluster')),
                ('object_apiVersion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='flux.fluxobjectapiversionmodel', verbose_name='api version')),
                ('object_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='flux.fluxobjectkindmodel', verbose_name='kind')),
                ('object_namespace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='flux.fluxobjectnamespacemodel', verbose_name='namespace')),
            ],
            options={
                'unique_together': {('cluster', 'object_uid')},
            },
        ),
    ]