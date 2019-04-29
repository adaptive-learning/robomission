from django.test import TestCase
import pytest
from learn.domain_parser import load_domain_from_file, parse_task_source
from learn.models import Domain, Task, ProblemSet
from learn.utils.text import unpad


#@pytest.fixture(scope='module')
#def domain():
#    load_domain_from_file('domain/tests/test1.domain.json')
#    domain = Domain.objects.get(name='test1')
#    # TODO: delete the domain (cascade)
#    return domain

class DomainParserTestCase(TestCase):
    # TODO: Use a fixture to avoid parsing the file multiple times, but still
    # having multiple unit tests for better readability.
    @pytest.mark.slow
    def test_load_domain_from_file(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        domain = Domain.objects.get(name='test1')

        # Test entities loaded
        self.assertQuerysetEqual(
            domain.blocks.all(),
            ['<Block: b1>', '<Block: b2>'])
        self.assertQuerysetEqual(
            domain.toolboxes.all(),
            ['<Toolbox: tb1>', '<Toolbox: tb2>'],
            ordered=False)
        self.assertQuerysetEqual(
            domain.tasks.all(),
            ['<Task: t1>', '<Task: t2>', '<Task: t3>'])
        self.assertQuerysetEqual(
            domain.problemsets.all(),
            # NOTE: PS are ordered by type first, which is different for
            # missions and phases.
            ['<ProblemSet: m1>', '<ProblemSet: m2>', '<ProblemSet: m3>',
             '<ProblemSet: m4>',
             '<ProblemSet: p1A>', '<ProblemSet: p1B>', '<ProblemSet: p1C>',
             '<ProblemSet: p2A>','<ProblemSet: p2B>', '<ProblemSet: p2C>'])
        self.assertQuerysetEqual(
            domain.instructions.all(),
            ['<Instruction: i1>', '<Instruction: i2>'])

        # Test inferred granularity and sections.
        p2c = ProblemSet.objects.get(name='p2C')
        assert p2c.granularity == ProblemSet.PHASE
        assert p2c.section == '2.3'
        assert p2c.order == 3
        assert p2c.level == 2

        # Test tasks content.
        task = Task.objects.get(pk=1)
        assert task.name == 't1'
        assert task.solution == 'f'
        assert task.setting == {'fields': 'b;kS'}
        assert task.section == '1.1.1'

        # Test relationships.
        p1b = ProblemSet.objects.get(name='p1B')
        self.assertQuerysetEqual(p1b.tasks.all(), ['<Task: t2>', '<Task: t3>'])

        # Test domain params.
        self.assertQuerysetEqual(
            domain.params.all(),
            ['<DomainParam: test1:good_time:task:t1=10.0>',
             '<DomainParam: test1:good_time:task:t2=20.0>',
             '<DomainParam: test1:good_time:task:t3=30.0>'],
            ordered=False)

    @pytest.mark.slow
    def test_load_domain_update_existing_task(self):
        domain = Domain.objects.create(name='test1')
        t1 = Task.objects.create(pk=1, name='t1-original')
        domain.tasks.set([t1])
        load_domain_from_file('domain/tests/test1.domain.json')
        t1 = Task.objects.get(name='t1')
        assert t1.pk == 1
        assert t1.name == 't1'
        assert t1.solution == 'f'
        assert not Task.objects.filter(name='t1-original').exists()

    @pytest.mark.slow
    def test_load_current_domain(self):
        load_domain_from_file('domain/domain.json')
        domain = Domain.objects.get(name='current')
        assert domain.blocks.exists()
        assert domain.toolboxes.exists()
        assert domain.tasks.exists()
        assert domain.instructions.exists()
        assert domain.params.exists()


    # The following test demonstrates currently not allowed behavior
    # (the test don't pass): it's not possible to rename a task to an existing
    # name, since that could easily lead to data inconsitencies. To load a new
    # domain on local/staging machine, it will be necessary to delete existing
    # data first (make reset_db), because the task IDs were set to match the
    # production DB.
    #def test_load_domain_swap_task_ids(self):
    #    domain = Domain.objects.create(name='test1')
    #    tA = Task.objects.create(pk=2, name='t1', setting='{}', solution='')
    #    tB = Task.objects.create(pk=1, name='t2', setting='{}', solution='')
    #    domain.tasks.set([tA, tB])
    #    load_domain_from_file('domain/tests/test1.domain.json')
    #    assert Task.objects.get(pk=1).name == 't1'
    #    assert Task.objects.get(pk=2).name == 't2'


@pytest.fixture(scope='session')
def task_text_scaffolding():
    return unpad('''
        # t4-scaffolding

        ## Setting
        - description: "Fly twice forward."

        ```
        |b |
        |k |
        |kS|
        ```

        ### Initial Code
        ```
        fly()
        ```

        ## Solution

        ```
        fly()
        fly()
        ```
        ''')


def test_parse_task_source_scaffolding(task_text_scaffolding):
    parsed_data = parse_task_source(task_text_scaffolding)
    expected_data = {
            'name': 't4-scaffolding',
            'setting': {
                'description': "Fly twice forward.",
                'fields': 'b;k;kS',
                'initial_code': 'f'
                },
            'solution': 'ff'
    }
    assert parsed_data == expected_data

