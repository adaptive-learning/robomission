from django.test import TestCase
from learn.domain_parser import load_domain_from_file
from learn.models import Domain, Task, Chunk


class DomainParserTestCase(TestCase):
    def test_load_domain_from_file__entities(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(
            domain.blocks.all(),
            ['<Block: b1>', '<Block: b2>'])
        self.assertQuerysetEqual(
            domain.toolboxes.all(),
            ['<Toolbox: tb1>', '<Toolbox: tb2>'],
            ordered=False)
        self.assertQuerysetEqual(
            domain.tasks.all(),
            ['<Task: t1>', '<Task: t2>', '<Task: t3>'],
            ordered=False)
        self.assertQuerysetEqual(
            domain.chunks.all(),
            ['<Chunk: c1a>', '<Chunk: c1b>', '<Chunk: c1c>', '<Chunk: c1>',
            '<Chunk: c2a>', '<Chunk: c2b>', '<Chunk: c2>'])
        self.assertQuerysetEqual(
            domain.missions.all(),
            ['<Mission: M1 m1 (c1)>', '<Mission: M2 m2 (c2)>'])

    def test_load_domain_from_file__tasks(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        task = Task.objects.get(pk=1)
        assert task.name == 't1'
        assert task.setting == '{"fields": [[["b", []]], [["k", ["S"]]]]}'
        assert task.solution == 'f'

    def test_load_domain_from_file__relationships(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        chunk = Chunk.objects.get(name='c1b')
        self.assertQuerysetEqual(
            chunk.tasks.all(),
            ['<Task: t2>', '<Task: t3>'],
            ordered=False)
