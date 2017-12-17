"""Setting for admin page.
"""
from django.contrib import admin
from learn.models import Block, Toolbox, Level, Task, Instruction, Student
from learn.models import TaskSession, ProgramSnapshot, Action, Feedback


@admin.register(TaskSession)
class TaskSessionAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'


@admin.register(ProgramSnapshot)
class ProgramSnapshotAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'inserted'


admin.site.register(Block)
admin.site.register(Toolbox)
admin.site.register(Level)
admin.site.register(Task)
admin.site.register(Instruction)
admin.site.register(Student)
