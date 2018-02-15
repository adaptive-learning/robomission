from django.test import TestCase
from learn.domain import load_domain_from_file
from learn.models import Domain


class DomainTestCase(TestCase):
    def test_load_domain_from_file(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(domain.blocks.all(), ['<Block: b1>', '<Block: b2>'])
        # TODO: test other entities
