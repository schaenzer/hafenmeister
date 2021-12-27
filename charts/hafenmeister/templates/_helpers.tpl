{{/* vim: set filetype=mustache: */}}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "hafenmeister.fullname" -}}
{{- printf "%s-%s" .Chart.Name .Release.Name | trunc 30 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a fully qualified component name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}

{{- define "hafenmeister.django.fullname" -}}
{{- printf "%s-django" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.celeryworker.fullname" -}}
{{- printf "%s-celeryworker" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.celerybeat.fullname" -}}
{{- printf "%s-celerybeat" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.celeryflower.fullname" -}}
{{- printf "%s-celeryflower" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.rabbitmq.fullname" -}}
{{- printf "%s-rabbitmq" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.mailhog.fullname" -}}
{{- printf "%s-mailhog" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.postgresql.fullname" -}}
{{- printf "%s-postgresql" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.staticfiles.fullname" -}}
{{- printf "%s-staticfiles" (include "hafenmeister.fullname" .) | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.gotenberg.fullname" -}}
{{- printf "%s-gotenberg" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.elasticsearch.fullname" -}}
{{- printf "%s-elasticsearch" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.google_service_account.fullname" -}}
{{- printf "%s-google-service-account" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "hafenmeister.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
Return the appropriate apiVersion for deployment.
*/}}
{{- define "hafenmeister.deployment.apiVersion" -}}
{{- if semverCompare "<1.14-0" .Capabilities.KubeVersion.GitVersion -}}
{{- print "extensions/v1beta1" -}}
{{- else -}}
{{- print "apps/v1" -}}
{{- end -}}
{{- end -}}


{{- define "hafenmeister.pod_environment" -}}
- name: DEPLOYMENT_VERSION
  value: "..."
- name: DEPLOYMENT_ENVIROMENT
  value: {{ .Release.Name | quote }}
- name: POD_IP
  valueFrom:
    fieldRef:
      fieldPath: status.podIP
- name: RABBITMQ_HOST
  value: {{ template "hafenmeister.rabbitmq.fullname" . }}
- name: RABBITMQ_USER
  valueFrom:
    secretKeyRef:
      name: {{ template "hafenmeister.rabbitmq.fullname" . }}-default-user
      key: username
- name: RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "hafenmeister.rabbitmq.fullname" . }}-default-user
      key: password
- name: POSTGRES_DB
  value: django
- name: POSTGRES_HOST
  value: {{ include "hafenmeister.postgresql.fullname" . }}
- name: POSTGRES_PORT
  value: "5432"
- name: POSTGRES_USER
  valueFrom:
    secretKeyRef:
      name: django.{{ template "hafenmeister.postgresql.fullname" . }}.credentials.postgresql.acid.zalan.do
      key: username
- name: POSTGRES_PASSWORD
  valueFrom:
    secretKeyRef:
      name: django.{{ template "hafenmeister.postgresql.fullname" . }}.credentials.postgresql.acid.zalan.do
      key: password
{{- if gt .Values.component.mailhog.replicaCount 0.0 }}
- name: DJANGO_EMAIL_HOST
  value: "{{ include "hafenmeister.mailhog.fullname" . }}"
{{- end -}}
{{- end -}}


{{/*
Create the name of the service account to use
*/}}
{{- define "hafenmeister.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "hafenmeister.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}



{{/*
Staticfiles
*/}}
{{- define "hafenmeister.staticfiles.enabled" -}}
{{- if gt .Values.component.staticfiles.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{/*
Mailhog
*/}}
{{- define "hafenmeister.mailhog.enabled" -}}
{{- if gt .Values.component.mailhog.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{/*
Celerybeat, Celeryworker & Celeryflower
*/}}
{{- define "hafenmeister.celerybeat.enabled" -}}
{{- if gt .Values.component.celerybeat.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{- define "hafenmeister.celeryworker.enabled" -}}
{{- if gt .Values.component.celeryworker.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{- define "hafenmeister.celeryflower.enabled" -}}
{{- if gt .Values.component.celeryflower.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{/*
Elasticsearch
*/}}
{{- define "hafenmeister.elasticsearch.enabled" -}}
{{- if gt .Values.component.elasticsearch.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{/*
Gotenberg
*/}}
{{- define "hafenmeister.gotenberg.enabled" -}}
{{- if gt .Values.component.gotenberg.replicaCount 0.0 }}
{{-   true }}
{{- else -}}
{{-   false }}
{{- end }}
{{- end -}}

{{/*
NetworkPolies
*/}}

{{- define "hafenmeister.networkPolicy.celeryflower.allowMetricFromExternal" -}}
{{- printf "%s-allow-celeryflower-metric-access-from-external" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.postgresql.cross" -}}
{{- printf "%s-allow-cross-psql" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.rabbitmq.cross" -}}
{{- printf "%s-allow-cross-rabbitmq" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.django.allowFromExternal" -}}
{{- printf "%s-allow-django-access-from-external" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.elasticsearch.allowAccess" -}}
{{- printf "%s-allow-elastic-access" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.gotenberg.allowAccess" -}}
{{- printf "%s-allow-gotenberg-access" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.mailhog.allowAccess" -}}
{{- printf "%s-allow-mailhog-access" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.postgresql.allowAccess" -}}
{{- printf "%s-allow-psql-access" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.rabbitmq.allowAccess" -}}
{{- printf "%s-allow-rabbitmq-access" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.mailhog.allowFromExternal" -}}
{{- printf "%s-allow-mailhog-access-from-external" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.staticfiles.allowFromExternal" -}}
{{- printf "%s-allow-staticfiles-access-from-external" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.postgresql.allowMetricFromExternal" -}}
{{- printf "%s-allow-psql-metric-access-from-external" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.postgresql.allowFromOperator" -}}
{{- printf "%s-allow-psql-access-from-operator" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hafenmeister.networkPolicy.defaultDeny" -}}
{{- printf "%s-default-deny" (include "hafenmeister.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
