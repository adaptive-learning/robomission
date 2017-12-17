"""Setting for admin page.
"""
from django.contrib import admin
from learn.models import Block, Toolbox, Level, Task, Instruction, Student
from learn.models import TaskSession, ProgramSnapshot, Action, Feedback

admin.site.register(Block)
admin.site.register(Toolbox)
admin.site.register(Level)
admin.site.register(Task)
admin.site.register(Instruction)
admin.site.register(Student)
admin.site.register(TaskSession)
admin.site.register(ProgramSnapshot)
admin.site.register(Action)
admin.site.register(Feedback)
