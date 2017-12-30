"""Settings for the admin page.
"""
from django.contrib import admin
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, ProgramSnapshot, Student, TaskSession, Feedback
from learn.admin import BlockAdmin, ToolboxAdmin, LevelAdmin, TaskAdmin, InstructionAdmin
from learn.admin import ActionAdmin, ProgramSnapshotAdmin, StudentAdmin
from learn.admin import TaskSessionAdmin, FeedbackAdmin
from monitoring.models import Metric


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'time', 'value')
    list_filter = ('name', 'group')
    search_fields = ('name', 'group')
    date_hierarchy = 'time'


class DataViewSite(admin.AdminSite):
    """Fork of admin site used for viewing data only, not editing.

    TODO: Enforce the view-only mode. Currently, it requires correct
    permissions for given staff member.
    """
    site_header = 'RoboMission Data View'
    site_title = 'RoboMission Data View'


data_view_site = DataViewSite(name='monitoring.data_view_site')
data_view_site.register(Block, BlockAdmin)
data_view_site.register(Instruction, InstructionAdmin)
data_view_site.register(Level, LevelAdmin)
data_view_site.register(Task, TaskAdmin)
data_view_site.register(Toolbox, ToolboxAdmin)
data_view_site.register(TaskSession, TaskSessionAdmin)
data_view_site.register(ProgramSnapshot, ProgramSnapshotAdmin)
data_view_site.register(Student, StudentAdmin)
data_view_site.register(Action, ActionAdmin)
data_view_site.register(Feedback, FeedbackAdmin)
data_view_site.register(Metric, MetricAdmin)
