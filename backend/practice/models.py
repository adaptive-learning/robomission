from django.db import models


class Block(models.Model):
    """Entity representing a programming block
    """
    name = models.CharField(max_length=256, unique=True)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
