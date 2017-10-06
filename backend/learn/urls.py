from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from learn import views


urlpatterns = [
    url(r'^blocks/$', views.block_list),
    url(r'^blocks/(?P<pk>[0-9]+)$', views.block_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
