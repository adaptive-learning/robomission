from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from monitoring.models import Metric
from monitoring.serializers import MetricSerializer


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer

    def get_queryset(self):
        n_days = int(self.request.query_params.get('days', 30))
        from_day = timezone.now().date() - timedelta(days=n_days)
        metrics = Metric.objects.filter(time__gte=from_day)
        return metrics
