from django.test import TestCase
from learn.models import Block, Toolbox, Task, ProblemSet, Domain
from learn.serializers import BlockSerializer, ToolboxSerializer, SettingSerializer
from learn.serializers import TaskSerializer, ProblemSetSerializer
from learn.serializers import DomainSerializer


class BlockSerializerTestCase(TestCase):
    def test_serialization(self):
        block = Block.objects.create(name='b1', order=5)
        serializer = BlockSerializer(block)
        assert serializer.data == {
            'id': block.id,
            'name': 'b1',
            'order': 5}

    def test_deserialization(self):
        data = {'id': 1001, 'name': 'b1', 'order': 5}
        serializer = BlockSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        block = serializer.save()
        block = Block.objects.get(id=1001)
        assert block.name == 'b1'
        assert block.order == 5

    def test_deserialize_list(self):
        domain = Domain.objects.create()
        data = [
            {'id': 2, 'name': 'b1'},
            {'id': 1, 'name': 'b2'}]
        serializer = BlockSerializer(many=True)
        serializer.set(domain.blocks, data)
        self.assertQuerysetEqual(
            domain.blocks.all(),
            ['<Block: b1>', '<Block: b2>'])

    def test_deserialize_order(self):
        domain = Domain.objects.create()
        data = [
            {'id': 2, 'name': 'b1'},
            {'id': 1, 'name': 'b2'}]
        serializer = BlockSerializer(many=True)
        serializer.set(domain.blocks, data)
        assert Block.objects.get(pk=2).order == 0
        assert Block.objects.get(pk=1).order == 1


class ToolboxSerializerTestCase(TestCase):
    def test_serialization(self):
        block1 = Block.objects.create(name='b1', order=1)
        block2 = Block.objects.create(name='b2', order=2)
        toolbox = Toolbox.objects.create(name='tb1')
        toolbox.blocks.set([block1, block2])
        serializer = ToolboxSerializer(toolbox)
        assert serializer.data == {
            'id': toolbox.id,
            'name': 'tb1',
            'blocks': ['b1', 'b2']}

    def test_deserialization(self):
        block1 = Block.objects.create(name='b1', order=1)
        block2 = Block.objects.create(name='b2', order=2)
        data = {
            'id': 21,
            'name': 'tb1',
            'blocks': ['b1', 'b2']}
        serializer = ToolboxSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        toolbox = Toolbox.objects.get(id=21)
        assert toolbox.name == 'tb1'
        assert list(toolbox.blocks.all()) == [block1, block2]

    def test_deserialize_list(self):
        domain = Domain.objects.create()
        Block.objects.create(name='b1', order=1)
        Block.objects.create(name='b2', order=2)
        data = [
            {'id': 21, 'name': 'tb1', 'blocks': ['b1']},
            {'id': 22, 'name': 'tb2', 'blocks': ['b2']}]
        serializer = ToolboxSerializer(many=True)
        serializer.set(domain.toolboxes, data)
        self.assertQuerysetEqual(
            domain.toolboxes.all(),
            ['<Toolbox: tb1>', '<Toolbox: tb2>'], ordered=False)

    def test_update_existing_toolbox(self):
        domain = Domain.objects.create()
        toolbox = Toolbox.objects.create(name='tb1')
        data = [{'id': toolbox.id, 'name': 'tb1n', 'blocks': []}]
        serializer = ToolboxSerializer(many=True)
        serializer.set(domain.toolboxes, data)
        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1n>'])

    def test_update_existing_toolbox_same_name(self):
        domain = Domain.objects.create()
        toolbox = Toolbox.objects.create(name='tb1')
        data = [{'id': toolbox.id, 'name': 'tb1', 'blocks': []}]
        serializer = ToolboxSerializer(many=True)
        serializer.set(domain.toolboxes, data)
        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1>'])


class SettingSerializerTestCase(TestCase):
    def test_available_fields(self):
        setting = {'toolbox': 'fly'}
        serializer = SettingSerializer(setting)
        assert serializer.data == setting

    def test_empty_setting_is_valid(self):
        serializer = SettingSerializer({})
        assert serializer.data == {}

    def test_deserialization(self):
        data = {'toolbox': 'fly'}
        serializer = SettingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {'toolbox': 'fly'}


class TaskSerializerTestCase(TestCase):
    def test_task_serialization(self):
        ps = ProblemSet.objects.create(name='ps1')
        task = Task.objects.create(
            name='carrot', section='2.3', problemset=ps,
            setting={'fields': 'kD|k||k|kS', 'length': 3, 'energy': 7},
            solution='f')
        serializer = TaskSerializer(task)
        assert serializer.data == {
            'id': task.pk,
            'name': 'carrot',
            'section': '2.3',
            'levels': [2, 3],
            'level': 2,
            'order': 3,
            'problemset': 'ps1',
            'setting': {'fields': 'kD|k||k|kS', 'length': 3, 'energy': 7},
            'solution': 'f'}

    def test_deserialize_new_task(self):
        data = {
            'id': 1,
            'name': 'carrot',
            'section': '2.3',
            'setting': {'toolbox': 'fly'},
            'solution': 'f'}
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        assert task.id == 1
        assert task.name == 'carrot'
        assert task.section == '2.3'
        assert task.solution == 'f'
        assert task.setting == {'toolbox': 'fly'}


class ProblemSetSerializerTestCase(TestCase):
    def test_ps_serialization(self):
        # TODO: test with a parent ps
        ps = ProblemSet.objects.create(
            name='wormholes', section='5.2', setting={'toolbox': 'fly'})
        serializer = ProblemSetSerializer(ps)
        assert serializer.data == {
            'id': ps.pk,
            'name': 'wormholes',
            'granularity': 'mission',
            'section': '5.2',
            'level': 5,
            'order': 2,
            'setting': {'toolbox': 'fly'},
            'parent': None,
            'tasks': [],
            'parts': []}

    def test_serialize_ps_with_default_setting(self):
        ps = ProblemSet.objects.create(name='wormholes')
        serializer = ProblemSetSerializer(ps)
        assert serializer.data == {
            'id': ps.pk,
            'name': 'wormholes',
            'granularity': 'mission',
            'section': '1',
            'level': 1,
            'order': 1,
            'setting': {},
            'parent': None,
            'tasks': [],
            'parts': []}

    def test_serialize_ps_with_tasks(self):
        task1 = Task.objects.create(id=1, name='t1')
        task2 = Task.objects.create(id=2, name='t2')
        ps = ProblemSet.objects.create(name='wormholes')
        ps.tasks.set([task1, task2])
        serializer = ProblemSetSerializer(ps)
        assert serializer.data['tasks'] == ['t1', 't2']

    def test_serialize_ps_with_parts(self):
        task1 = Task.objects.create(id=1, name='t1')
        task2 = Task.objects.create(id=2, name='t2')
        ps1 = ProblemSet.objects.create(name='ps1')
        ps2 = ProblemSet.objects.create(name='ps2')
        ps1.tasks.set([task1])
        ps1.parts.set([ps2])
        ps2.tasks.set([task2])
        serializer = ProblemSetSerializer(ps1)
        assert serializer.data['id'] == ps1.pk
        assert serializer.data['name'] == 'ps1'
        assert serializer.data['parts'] == ['ps2']

    def test_serialize_multiple_chunks(self):
        ps1 = ProblemSet.objects.create(name='ps1')
        ps2 = ProblemSet.objects.create(name='ps2')
        pss = ProblemSet.objects.filter(name__in=['ps1', 'ps2'])
        serializer = ProblemSetSerializer(pss, many=True)
        assert len(serializer.data) == 2
        assert serializer.data[0]['name'] == 'ps1'
        assert serializer.data[1]['name'] == 'ps2'
        # TODO: check order/sections

    def test_deserialize_new_ps(self):
        data = {
            'id': 1,
            'name': 'wormholes',
            'setting': {'toolbox': 'fly'}}
        serializer = ProblemSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        assert ps.id is not None
        assert ps.name == 'wormholes'
        # TODO: test section/order: assert ps.order == 5
        assert ps.setting == {'toolbox': 'fly'}
        assert ps.tasks.count() == 0
        assert ps.parts.count() == 0

    def test_deserialize_ps_without_setting(self):
        data = {'id': 1, 'name': 'wormholes'}
        serializer = ProblemSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        assert ps.setting == {}

    def test_deserialize_new_ps_with_tasks(self):
        task1 = Task.objects.create(id=1, name='t1')
        data = {
            'id': 1,
            'name': 'wormholes',
            'setting': {'toolbox': 'fly'},
            'tasks': ['t1']}
        serializer = ProblemSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        assert list(ps.tasks.all()) == [task1]

    def test_update_existing_ps(self):
        task1 = Task.objects.create(id=1, name='t1')
        ps = ProblemSet.objects.create(id=2, name='ps1')
        data = {
            'id': 2,
            'name': 'ps2',
            'setting': {'toolbox': 'fly'},
            'tasks': ['t1']}
        serializer = ProblemSetSerializer(ps, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        ps_db = ProblemSet.objects.get(pk=2)
        assert ps == ps_db
        assert ps_db.name == 'ps2'
        assert ps_db.setting == {'toolbox': 'fly'}
        assert list(ps_db.tasks.all()) == [task1]

    def test_change_tasks_of_existing_ps(self):
        ps = ProblemSet.objects.create(name='ps1')
        ps.add_task(name='t1')
        t2 = ps.add_task(name='t2')
        t3 = Task.objects.create(name='t3')
        data = {
            'name': 'ps1',
            'tasks': ['t2', 't3']}
        serializer = ProblemSetSerializer(ps, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        ps_db = ProblemSet.objects.get(name='ps1')
        assert ps == ps_db
        assert set(ps_db.tasks.all()) == {t2, t3}

    def test_change_parts_of_existing_ps(self):
        ps1 = ProblemSet.objects.create(id=1, name='ps1')
        ps2 = ProblemSet.objects.create(id=2, name='ps2')
        ps3 = ProblemSet.objects.create(id=3, name='ps3')
        ps4 = ProblemSet.objects.create(id=4, name='ps4')
        ps1.parts.set([ps2, ps3])
        data = {
            'name': 'ps1',
            'parts': ['ps3', 'ps4']}
        serializer = ProblemSetSerializer(ps1, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        ps_db = ProblemSet.objects.get(pk=1)
        assert ps == ps_db
        assert set(ps_db.parts.all()) == {ps3, ps4}

    def test_deserialize_list_of_new_ps(self):
        domain = Domain.objects.create()
        data = [{'id': 1, 'name': 'ps1'}, {'id': 2, 'name': 'ps2'}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        ps1 = ProblemSet.objects.get(pk=1)
        ps2 = ProblemSet.objects.get(pk=2)
        assert ps1.name == 'ps1'
        assert ps1.order == 1
        assert ps2.name == 'ps2'
        assert ps2.order == 2

    def test_deserialize_list_of_new_ps_with_parts(self):
        domain = Domain.objects.create()
        data = [
            {'id': 1, 'name': 'ps1'},
            {'id': 2, 'name': 'ps2', 'parts': ['ps1']}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        # TODO:
        #chunk2 = ProblemSet.objects.get(pk=2)
        #self.assertQuerysetEqual(chunk2.subchunks.all(), ['<ProblemSet c1>'])

    def test_deserialize_list_of_new_chunks__update_existing(self):
        domain = Domain.objects.create()
        ps = ProblemSet.objects.create(id=2, name='ps2', section='5')
        data = [
            {'id': 1, 'name': 'ps1'},
            {'id': 2, 'name': 'ps2-v2', 'section': '7'}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        ps = ProblemSet.objects.get(pk=2)
        assert ps.name == 'ps2-v2'
        assert ps.section == '7'

    def test_deserialize_list_of_new_chunks__remove_old(self):
        domain = Domain.objects.create()
        ProblemSet.objects.create(id=2, name='c2')
        data = [{'id': 1, 'name': 'c1'}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        assert {chunk.pk for chunk in domain.problemsets.all()} == {1}

    def test_serialize_mission_with_phases(self):
        m1 = ProblemSet.objects.create(name='m1', section='2.3')
        p1 = m1.add_part(name='p1')
        p2 = m1.add_part(name='p2')
        serializer = ProblemSetSerializer(m1)
        assert serializer.data == {
            'id': m1.pk,
            'name': 'm1',
            'granularity': 'mission',
            'parent': None,
            'section': '2.3',
            'level': 2,
            'order': 3,
            'setting': {},
            'parts': ['p1', 'p2'],
            'tasks': []}

    def test_deserialize_new_mission(self):
        data = {
            "id": 2,
            "name": "m1",
            "setting": { "toolbox": "tb1" }}
        serializer = ProblemSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        mission = serializer.save()
        assert mission.id == 2
        assert mission.name == 'm1'
        assert mission.section == '1'
        assert mission.setting == { "toolbox": "tb1" }

    def test_update_existing_mission(self):
        m1 = ProblemSet.objects.create(pk=1, name='m1')
        p1 = ProblemSet.objects.create(pk=2, name='p1', parent=m1)
        data = {
            "id": 1,
            "name": "m1n",
            "setting": { "toolbox": "tb1" },
            "parts": [ "p1" ]}
        serializer = ProblemSetSerializer(m1, data=data)
        serializer.is_valid(raise_exception=True)
        m1 = serializer.save()
        assert m1.id == 1
        assert m1.name == 'm1n'
        assert m1.setting == { "toolbox": "tb1" }
        assert list(m1.parts.all()) == [p1]

    def test_deserialize_list_of_new_missions(self):
        data = [
            {'id': 1, 'name': 'm1'},
            {'id': 2, 'name': 'm2'}]
        domain = Domain.objects.create()
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        problemsets = list(domain.problemsets.all())
        assert len(problemsets) == 2
        assert problemsets[0].name == 'm1'
        assert problemsets[0].section == '1'
        assert problemsets[1].name == 'm2'
        assert problemsets[1].section == '2'

    def test_deserialize_list_of_new_missions__update_existing(self):
        domain = Domain.objects.create()
        m1 = ProblemSet.objects.create(pk=1, name='m1')
        data = [
            {'id': 1, 'name': 'm1n'},
            {'id': 2, 'name': 'm2'}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        problemsets = list(domain.problemsets.all())
        assert len(problemsets) == 2
        assert problemsets[0].name == 'm1n'
        assert problemsets[0].section == '1'
        assert problemsets[1].name == 'm2'
        assert problemsets[1].section == '2'

    def test_deserialize_list_of_new_missions__delete_existing(self):
        domain = Domain.objects.create()
        m1 = ProblemSet.objects.create(pk=1, name='m1')
        data = [{'id': 2, 'name': 'm2'}]
        serializer = ProblemSetSerializer(many=True)
        serializer.set(domain.problemsets, data)
        problemsets = list(domain.problemsets.all())
        assert len(problemsets) == 1
        assert problemsets[0].name == 'm2'


class DomainSerializerTestCase(TestCase):
    def test_nested_serialization(self):
        block = Block.objects.create(name='b1', order=5)
        toolbox = Toolbox.objects.create(name='tb1')
        toolbox.blocks.set([block])
        domain = Domain.objects.create(name='d1')
        domain.blocks.set([block])
        domain.toolboxes.set([toolbox])
        serializer = DomainSerializer(domain)
        assert serializer.data == {
            'name': 'd1',
            'blocks': [{'id': block.id, 'name': 'b1', 'order': 5}],
            'toolboxes': [{'id': toolbox.id, 'name': 'tb1', 'blocks': ['b1']}],
            'tasks': [], 'problemsets': []}

    def test_nested_deserialization(self):
        data = {
            "name": "test1", "problemsets" : [], "tasks": [],
            "toolboxes": [{"id": 1, "name": "tb1", "blocks": ["b1", "b2"]}],
            "blocks": [{"id": 1, "name": "b1"}, {"id": 2, "name": "b2"}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(
            domain.toolboxes.first().blocks.all(),
            ['<Block: b1>', '<Block: b2>'])

    def test_domain_with_hierarchical_ps_deserialization(self):
        data = {
            "name": "test1", "blocks" : [], "toolboxes": [], "tasks": [],
            "problemsets": [
                {"id": 1, "name": "m1", "parts": ["p1"]},
                {"id": 2, "name": "p1"}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        m1 = domain.problemsets.get(name='m1')
        assert m1.name == 'm1'
        assert m1.section == '1'
        assert m1.parts.count() == 1
        assert m1.parts.first().name == 'p1'

    def test_update_existing_domain(self):
        block = Block.objects.create(name='b1', order=5)
        domain = Domain.objects.create(name='test1')
        domain.blocks.set([block])
        data = {
            "name": "test1",
            "problemsets" : [], "tasks": [], "toolboxes": [],
            "blocks": [{"id": block.id, "name": "b2"}, {"id": 3, "name": "b3"}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(
            domain.blocks.all(),
            ['<Block: b2>', '<Block: b3>'])

    def test_update_existing_domain_with_toolbox(self):
        toolbox = Toolbox.objects.create(name='tb1')
        domain = Domain.objects.create(name='test1')
        domain.toolboxes.set([toolbox])
        data = {
            "name": "test1",
            "problemsets" : [], "tasks": [], "blocks": [],
            "toolboxes": [{"id": toolbox.pk, "name": "tb1n", "blocks": []}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1n>'])

    def test_update_existing_domain_nested(self):
        block = Block.objects.create(name='b1', order=5)
        toolbox = Toolbox.objects.create(name='tb1')
        toolbox.blocks.set([block])
        domain = Domain.objects.create(name='test1')
        domain.blocks.set([block])
        domain.toolboxes.set([toolbox])
        data = {
            "name": "test1", "problemsets" : [], "tasks": [],
            "toolboxes": [{"id": toolbox.pk, "name": "tb1", "blocks": ["b2", "b3"]}],
            "blocks": [{"id": 2, "name": "b2"}, {"id": 3, "name": "b3"}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(
            domain.toolboxes.all(),
            ['<Toolbox: tb1>'])
        self.assertQuerysetEqual(
            domain.toolboxes.first().blocks.all(),
            ['<Block: b2>', '<Block: b3>'])

    def test_update_domain_same_names(self):
        """Test that no uniqeue name constraint error is raised when updating
           and existing entity, leaving its name same.
        """
        block = Block.objects.create(name='b1', order=5)
        toolbox = Toolbox.objects.create(name='tb1')
        ps = ProblemSet.objects.create(name='ps')
        domain = Domain.objects.create(name='test1')
        domain.blocks.set([block])
        domain.toolboxes.set([toolbox])
        domain.problemsets.set([ps])
        data = {
            "name": "test1",
            "problemsets" : [{"id": ps.pk, "name": "ps"}],
            "tasks": [],
            "toolboxes": [{"id": toolbox.pk, "name": "tb1", "blocks": []}],
            "blocks": [{"id": block.id, "name": "b1"}]}
        serializer = DomainSerializer()
        serializer.create_or_update(data)
        domain = Domain.objects.get(name='test1')
        self.assertQuerysetEqual(domain.blocks.all(), ['<Block: b1>'])
        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1>'])
        self.assertQuerysetEqual(domain.problemsets.all(), ['<ProblemSet: ps>'])
