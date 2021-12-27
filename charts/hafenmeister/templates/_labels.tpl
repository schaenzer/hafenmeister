{{- define "hafenmeister.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ include "hafenmeister.chart" . }}
{{- end -}}

{{- define "hafenmeister.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}


# Django

{{- define "hafenmeister.labels.django" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: django
{{- end -}}

{{- define "hafenmeister.selectorLabels.django" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: django
{{- end -}}


# Celeryworker

{{- define "hafenmeister.labels.celeryworker" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: celeryworker
{{- end -}}

{{- define "hafenmeister.selectorLabels.celeryworker" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: celeryworker
{{- end -}}


# Celerybeat

{{- define "hafenmeister.labels.celerybeat" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: celerybeat
{{- end -}}

{{- define "hafenmeister.selectorLabels.celerybeat" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: celerybeat
{{- end -}}


# Celeryflower

{{- define "hafenmeister.labels.celeryflower" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: celeryflower
{{- end -}}

{{- define "hafenmeister.selectorLabels.celeryflower" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: celeryflower
{{- end -}}


# staticfiles

{{- define "hafenmeister.labels.staticfiles" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: staticfiles
{{- end -}}

{{- define "hafenmeister.selectorLabels.staticfiles" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: staticfiles
{{- end -}}


# Mailhog

{{- define "hafenmeister.labels.mailhog" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: mailhog
{{- end -}}

{{- define "hafenmeister.selectorLabels.mailhog" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: mailhog
{{- end -}}


# postgresql

{{- define "hafenmeister.labels.postgresql" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: postgresql
{{- end -}}


# Other Services

{{- define "hafenmeister.labels.redis" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: redis
{{- end -}}

{{- define "hafenmeister.labels.renderer" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: renderer
{{- end -}}

{{- define "hafenmeister.selectorLabels.renderer" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: renderer
{{- end -}}

{{- define "hafenmeister.labels.gotenberg" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: gotenberg
{{- end -}}

{{- define "hafenmeister.selectorLabels.gotenberg" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: gotenberg
{{- end -}}

{{- define "hafenmeister.labels.rabbitmq" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: rabbitmq
{{- end -}}

{{- define "hafenmeister.labels.elasticsearch" -}}
{{- printf "%s\n" (include "hafenmeister.labels" .) -}}
app.kubernetes.io/component: elasticsearch
{{- end -}}

{{- define "hafenmeister.selectorLabels.elasticsearch" -}}
{{- printf "%s\n" (include "hafenmeister.selectorLabels" .) -}}
app.kubernetes.io/component: elasticsearch
{{- end -}}
