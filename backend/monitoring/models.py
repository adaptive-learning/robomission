"""Database entities for monitoring app.
"""
from datetime import date
from django.contrib.auth.models import User
from django.db import models


class Metric(models.Model):
    """Values we measure and report to check the system behavior

    Examples: number of daily active users, number of daily solved tasks.
    """
    name = models.CharField(
        max_length=256, null=False, blank=False)
    group = models.CharField(
        max_length=256, null=True, blank=True,
        help_text='Name of an experiment group, task, or other specific item.')
    time = models.DateField(default=date.today)
    value = models.FloatField()

    class Meta:
        ordering = ['time']
        unique_together = ('name', 'group', 'time')

    @property
    def full_name(self):
        if self.group:
            return '{name}.{group}'.format(name=self.name, group=self.group)
        return self.name

    def __str__(self):
        return '{name}@{time}={value}'.format(
            name=self.full_name,
            time=self.time,
            value=self.value)


class Feedback(models.Model):
    """Feedback message provided by a user.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField(null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    inserted = models.DateTimeField(auto_now_add=True)

    @property
    def comment_shortened(self):
        if len(self.comment) > 60:
            return self.comment[:60] + '...'
        return self.comment

    def __str__(self):
        return '[{pk}] {comment}'.format(
            pk=self.pk,
            comment=self.comment_shortened)
