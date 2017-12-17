"""Setting for admin page.
"""
from django.contrib import admin
from learn.models import Block, Toolbox, Level, Task, Instruction, Student
from learn.models import TaskSession, ProgramSnapshot, Action, Feedback


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'toolbox', 'credits')
    list_display_links = ('level', 'name')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')
    list_display_links = ('id', 'name')
    list_filter = ('level',)


@admin.register(Toolbox)
class ToolboxAdmin(admin.ModelAdmin):
    list_filter = ('blocks',)


@admin.register(TaskSession)
class TaskSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'task', 'solved', 'start', 'end')
    date_hierarchy = 'start'
    list_filter = ('task', 'solved', 'start')


@admin.register(ProgramSnapshot)
class ProgramSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_session', 'program', 'granularity', 'correct')
    date_hierarchy = 'time'
    list_filter = ('granularity', 'correct')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_filter = ('name',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'inserted'
    list_filter = ('inserted', 'url')


admin.site.register(Block)
admin.site.register(Instruction)
admin.site.register(Student)
