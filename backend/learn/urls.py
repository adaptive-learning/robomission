from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from learn import views


urlpatterns = [
    url(r'^blocks/$', views.BlockList.as_view()),
    url(r'^blocks/(?P<pk>[0-9]+)$', views.BlockDetail.as_view()),
    url(r'^toolboxes/$', views.ToolboxList.as_view()),
    url(r'^toolboxes/(?P<pk>[0-9]+)$', views.ToolboxDetail.as_view()),
    url(r'^students/$', views.StudentList.as_view()),
    url(r'^students/(?P<pk>[0-9]+)$', views.StudentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
