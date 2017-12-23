from rest_framework import viewsets
from monitoring.models import Metric
from monitoring.serializers import MetricSerializer


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
