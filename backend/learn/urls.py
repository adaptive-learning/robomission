from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from learn import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^blocks/$', views.BlockList.as_view()),
    url(r'^blocks/(?P<pk>[0-9]+)$', views.BlockDetail.as_view()),
    url(r'^toolboxes/$', views.ToolboxList.as_view()),
    url(r'^toolboxes/(?P<pk>[0-9]+)$', views.ToolboxDetail.as_view()),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^students/$', views.StudentList.as_view(), name='student-list'),
    url(r'^students/(?P<pk>[0-9]+)$', views.StudentDetail.as_view(), name='student-detail'),
    url(r'^students/(?P<pk>[0-9]+)/practice-overview/$', views.PracticeOverview.as_view(), name='practice-overview'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
