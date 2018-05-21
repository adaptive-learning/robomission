"""Utils for working with the domain.
"""
from django.db.models import Prefetch
from learn.models import ProblemSet, Domain


def get_domain(name='current'):
    """Return a prefeteched domain instance.
    """
    # TODO: Cache domain - it's used in almost all views.
    prefetches = [
        'params', 'blocks', 'toolboxes__blocks', 'tasks__problemset',
        Prefetch(
            'problemsets',
            queryset=ProblemSet.objects
                .select_related('parent')
                .prefetch_related('tasks', 'parts'))]
    domain = Domain.objects.prefetch_related(*prefetches).get(name=name)
    return domain
