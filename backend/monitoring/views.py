from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions
from rest_framework import viewsets
from learn.permissions import IsOwnerOrAdmin
from monitoring.models import Feedback, Metric
from monitoring.serializers import FeedbackSerializer, MetricSerializer
from monitoring import feedback


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated() else None
        new_feedback = serializer.save(user=user)
        feedback.log_and_send(new_feedback)


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        n_days = int(self.request.query_params.get('days', 30))
        from_day = timezone.now().date() - timedelta(days=n_days)
        metrics = Metric.objects.filter(time__gte=from_day)
        return metrics
