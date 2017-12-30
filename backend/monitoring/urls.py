from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
import monitoring.views
from monitoring.admin import data_view_site


api_router = DefaultRouter()
api_router.register(r'metrics', monitoring.views.MetricViewSet, base_name='metric')


urlpatterns = [
    url(r'^api/', include(api_router.urls)),
    url(r'^data-view/', data_view_site.urls),
]
