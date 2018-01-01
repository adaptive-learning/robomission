from monitoring.models import Feedback, Metric
from rest_framework import serializers


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')
    class Meta:
        model = Feedback
        fields = ('id', 'user', 'email', 'comment', 'url')


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('name', 'group', 'time', 'value')
