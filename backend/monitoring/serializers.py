from monitoring.models import Metric
from rest_framework import serializers


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('name', 'group', 'time', 'value')
