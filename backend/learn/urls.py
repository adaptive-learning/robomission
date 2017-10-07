from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learn import views


router = DefaultRouter()
router.register(r'blocks', views.BlockViewSet)
router.register(r'toolboxes', views.ToolboxViewSet)
router.register(r'levels', views.LevelViewSet)
router.register(r'instructions', views.InstructionViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'students', views.StudentViewSet, base_name='student')


urlpatterns = [
    url(r'^api/', include(router.urls)),
]
