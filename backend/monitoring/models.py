"""Database entities for monitoring app.
"""
from datetime import date
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
        return '{name}.{group}'.format(name=self.name, group=self.group)

    def __str__(self):
        return '{name}@{date}={value}'.format(
            name=self.full_name,
            date=self.date,
            value=self.value)
