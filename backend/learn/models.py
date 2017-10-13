"""DB entities definitions.
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class Block(models.Model):
    """Programming block, such as "fly" or "repeat".
    """
    name = models.CharField(max_length=256, unique=True)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Toolbox(models.Model):
    """Set of programming blocks
    """
    name = models.CharField(max_length=256, unique=True)
    blocks = models.ManyToManyField(Block)

    def __str__(self):
        return self.name


class Level(models.Model):
    """Small group of coherent tasks of similar difficulty sharing same toolbox.
    """
    level = models.SmallIntegerField()
    name = models.SlugField(unique=True)
    toolbox = models.ForeignKey(Toolbox)
    credits = models.IntegerField(
        help_text="Number of credits needed to complete this level.")
    # tasks = 1:n relation, see learn.models.Task

    def __str__(self):
        return 'L{level} {name}'.format(level=self.level, name=self.name)


class Instruction(models.Model):
    """Explanation of a single concept, such as while loop or wormholes.
    """
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Programming problem to be solved by students.
    """
    name = models.SlugField(max_length=100, unique=True)
    level = models.ForeignKey(Level, null=True, default=None, related_name='tasks')
    setting = JSONField()
    solution = JSONField()
    # sessions = m:n relation with students through learn.TaskSession

    def __str__(self):
        return self.name


class Student(models.Model):
    """Entity for a learner.
    """
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    seen_instructions = models.ManyToManyField(Instruction)
    # task_sessions = m:n relation with tasks through learn.TaskSession

    def __str__(self):
        return '[{pk}] {username}'.format(pk=self.pk, username=self.user.username)


class TaskSession(models.Model):
    """Continous attempt of a student to solve a task.
    """
    student = models.ForeignKey(Student, related_name='task_sessions')
    task = models.ForeignKey(Task, related_name='sessions')
    solved = models.BooleanField(default=False)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return '[{pk}] s{student}-{task}'.format(
            pk=self.pk,
            student=self.student.pk,
            task=self.task.name)
