from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
import monitoring.views


api_router = DefaultRouter()
api_router.register(r'metrics', monitoring.views.MetricViewSet, base_name='metric')
api_router.register(r'feedback', monitoring.views.FeedbackViewSet, base_name='feedback')


urlpatterns = [
    url(r'^api/', include(api_router.urls)),
]
