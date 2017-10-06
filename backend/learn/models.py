from django.db import models
from django.contrib.auth.models import User


class Block(models.Model):
    """Entity for a programming block
    """
    name = models.CharField(max_length=256, unique=True)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Toolbox(models.Model):
    """Entity for a set of programming blocks
    """
    name = models.CharField(max_length=256, unique=True)
    blocks = models.ManyToManyField(Block)

    def __str__(self):
        return self.name


class Student(models.Model):
    """Entity for a learner
    """
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return '[{pk}] {username}'.format(pk=self.pk, username=self.user.username)
