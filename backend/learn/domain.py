"""Utils for working with the domain.
"""
from django.db.models import Prefetch
from learn.models import Mission, Chunk, Domain


def get_domain(name='current'):
    """Return a prefeteched domain instance.
    """
    # TODO: Cache domain - it's used in almost all views.
    prefetches = [
        'blocks', 'toolboxes__blocks', 'tasks',
        Prefetch(
            'missions',
            queryset=Mission.objects.select_related('chunk')),
        Prefetch(
            'chunks',
            queryset=Chunk.objects.prefetch_related('tasks', 'subchunks'))]
    domain = Domain.objects.prefetch_related(*prefetches).get(name=name)
    return domain
