# Generated by Django 3.2.10 on 2021-12-29 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flux', '0005_alter_fluxobjectmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluxeventmodel',
            name='associated_transaction',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flux.fluxwebhooktransactionmodel'),
        ),
    ]
