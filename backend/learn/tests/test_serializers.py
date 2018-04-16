from django.test import TestCase
from learn.models import Block, Toolbox, Task, ProblemSet, Domain
from learn.serializers import BlockSerializer, ToolboxSerializer, SettingSerializer
from learn.serializers import ProblemSetSerializer
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
            'section': '0',
            'level': 0,
            'order': 0,
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
        ps1 = ProblemSet.objects.create(id=1, name='ps1', section='1')
        ps2 = ProblemSet.objects.create(id=2, name='ps2', section='2')
        ps3 = ProblemSet.objects.create(id=3, name='ps3', section='3')
        ps4 = ProblemSet.objects.create(id=4, name='ps4', section='4')
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
        assert ps1.order == 0
        assert ps2.name == 'ps2'
        # TODO: test correct order/section set automatically: assert ps2.order == 1

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

#class MissionSerializerTestCase(TestCase):
#    def test_serialize_mission_with_phases(self):
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        mission = Mission.objects.create(name='loops', chunk=chunk1, order=5)
#        serializer = MissionSerializer(mission)
#        assert serializer.data == {
#            'id': mission.pk,
#            'order': 5,
#            'name': 'loops',
#            'chunk': 'c1'}
#
#    def test_deserialize_new_mission(self):
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        data = {
#            "id": 1,
#            "name": "m1",
#            "chunk": "c1"}
#        serializer = MissionSerializer(data=data)
#        serializer.is_valid(raise_exception=True)
#        mission = serializer.save(order=2)
#        assert mission.id == 1
#        assert mission.name == 'm1'
#        assert mission.order == 2
#
#    def test_update_existing_mission(self):
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        chunk2 = ProblemSet.objects.create(name='c2', order=2)
#        mission = Mission.objects.create(id=1, name='m1', chunk=chunk1)
#        data = {
#            "id": 1,
#            "name": "m1n",
#            "chunk": "c2"}
#        serializer = MissionSerializer(mission, data=data)
#        serializer.is_valid(raise_exception=True)
#        mission = serializer.save(order=5)
#        mission_db = Mission.objects.get(pk=1)
#        assert mission == mission_db
#        assert mission.name == 'm1n'
#        assert mission.order == 5
#
#    def test_deserialize_list_of_new_missions(self):
#        domain = Domain.objects.create()
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        chunk2 = ProblemSet.objects.create(name='c2', order=2)
#        data = [
#            {'id': 1, 'name': 'm1', 'chunk': 'c1'},
#            {'id': 2, 'name': 'm2', 'chunk': 'c2'}]
#        serializer = MissionSerializer(many=True)
#        serializer.set(domain.missions, data)
#        missions = list(domain.missions.all())
#        assert len(missions) == 2
#        assert missions[0].name == 'm1'
#        assert missions[0].order == 1
#        assert missions[0].chunk == chunk1
#        assert missions[1].name == 'm2'
#        assert missions[1].order == 2
#        assert missions[1].chunk == chunk2
#
#    def test_deserialize_list_of_new_missions__update_existing(self):
#        domain = Domain.objects.create()
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        chunk2 = ProblemSet.objects.create(name='c2', order=2)
#        Mission.objects.create(id=1, name='m1', chunk=chunk1)
#        data = [{'id': 1, 'name': 'm1n', 'chunk': 'c2'}]
#        serializer = MissionSerializer(many=True)
#        serializer.set(domain.missions, data)
#        missions = list(domain.missions.all())
#        assert len(missions) == 1
#        assert missions[0].id == 1
#        assert missions[0].name == 'm1n'
#        assert missions[0].order == 1
#        assert missions[0].chunk == chunk2
#
#    def test_deserialize_list_of_new_missions__delete_existing(self):
#        domain = Domain.objects.create()
#        chunk1 = ProblemSet.objects.create(name='c1', order=1)
#        chunk2 = ProblemSet.objects.create(name='c2', order=2)
#        Mission.objects.create(id=1, name='m1', chunk=chunk1)
#        data = [{'id': 2, 'name': 'm2', 'chunk': 'c2'}]
#        serializer = MissionSerializer(many=True)
#        serializer.set(domain.missions, data)
#        missions = list(domain.missions.all())
#        assert len(missions) == 1
#        assert missions[0].id == 2
#        assert missions[0].name == 'm2'
#        assert missions[0].order == 1
#        assert missions[0].chunk == chunk2


#class DomainSerializerTestCase(TestCase):
#    def test_nested_serialization(self):
#        block = Block.objects.create(name='b1', order=5)
#        toolbox = Toolbox.objects.create(name='tb1')
#        toolbox.blocks.set([block])
#        domain = Domain.objects.create(name='d1')
#        domain.blocks.set([block])
#        domain.toolboxes.set([toolbox])
#        serializer = DomainSerializer(domain)
#        assert serializer.data == {
#            'name': 'd1',
#            'blocks': [{'id': block.id, 'name': 'b1', 'order': 5}],
#            'toolboxes': [{'id': toolbox.id, 'name': 'tb1', 'blocks': ['b1']}],
#            'tasks': [], 'chunks': [], 'missions': []}
#
#    def test_nested_deserialization(self):
#        data = {
#            "name": "test1", "missions" : [], "chunks": [], "tasks": [],
#            "toolboxes": [{"id": 1, "name": "tb1", "blocks": ["b1", "b2"]}],
#            "blocks": [{"id": 1, "name": "b1"}, {"id": 2, "name": "b2"}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(
#            domain.toolboxes.first().blocks.all(),
#            ['<Block: b1>', '<Block: b2>'])
#
#    def test_mission_with_chunk_deserialization(self):
#        data = {
#            "name": "test1", "blocks" : [], "toolboxes": [], "tasks": [],
#            "chunks": [{"id": 1, "name": "c1"}],
#            "missions": [{"id": 1, "name": "m1", "chunk": "c1"}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        mission = domain.missions.first()
#        assert mission.name == 'm1'
#
#    def test_update_existing_domain(self):
#        block = Block.objects.create(name='b1', order=5)
#        domain = Domain.objects.create(name='test1')
#        domain.blocks.set([block])
#        data = {
#            "name": "test1",
#            "missions" : [], "chunks": [], "tasks": [], "toolboxes": [],
#            "blocks": [{"id": block.id, "name": "b2"}, {"id": 3, "name": "b3"}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(
#            domain.blocks.all(),
#            ['<Block: b2>', '<Block: b3>'])
#
#    def test_update_existing_domain_with_toolbox(self):
#        toolbox = Toolbox.objects.create(name='tb1')
#        domain = Domain.objects.create(name='test1')
#        domain.toolboxes.set([toolbox])
#        data = {
#            "name": "test1",
#            "missions" : [], "chunks": [], "tasks": [], "blocks": [],
#            "toolboxes": [{"id": toolbox.pk, "name": "tb1n", "blocks": []}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1n>'])
#
#    def test_update_existing_domain_nested(self):
#        block = Block.objects.create(name='b1', order=5)
#        toolbox = Toolbox.objects.create(name='tb1')
#        toolbox.blocks.set([block])
#        domain = Domain.objects.create(name='test1')
#        domain.blocks.set([block])
#        domain.toolboxes.set([toolbox])
#        data = {
#            "name": "test1", "missions" : [], "chunks": [], "tasks": [],
#            "toolboxes": [{"id": toolbox.pk, "name": "tb1", "blocks": ["b2", "b3"]}],
#            "blocks": [{"id": 2, "name": "b2"}, {"id": 3, "name": "b3"}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(
#            domain.toolboxes.all(),
#            ['<Toolbox: tb1>'])
#        self.assertQuerysetEqual(
#            domain.toolboxes.first().blocks.all(),
#            ['<Block: b2>', '<Block: b3>'])
#
#    def test_update_domain_same_names(self):
#        block = Block.objects.create(name='b1', order=5)
#        toolbox = Toolbox.objects.create(name='tb1')
#        chunk = ProblemSet.objects.create(name='c1')
#        mission = Mission.objects.create(name='m1', chunk=chunk)
#        domain = Domain.objects.create(name='test1')
#        domain.blocks.set([block])
#        domain.toolboxes.set([toolbox])
#        domain.problemsets.set([chunk])
#        domain.missions.set([mission])
#        data = {
#            "name": "test1",
#            "missions" : [{"id": mission.pk, "name": "m1", "chunk": "c1"}],
#            "chunks" : [{"id": chunk.pk, "name": "c1"}],
#            "tasks": [],
#            "toolboxes": [{"id": toolbox.pk, "name": "tb1", "blocks": []}],
#            "blocks": [{"id": block.id, "name": "b1"}]}
#        serializer = DomainSerializer()
#        serializer.create_or_update(data)
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(domain.blocks.all(), ['<Block: b1>'])
#        self.assertQuerysetEqual(domain.toolboxes.all(), ['<Toolbox: tb1>'])
#        self.assertQuerysetEqual(domain.problemsets.all(), ['<ProblemSet: c1>'])
#        self.assertQuerysetEqual(domain.missions.all(), ['<Mission: M1 m1 (c1)>'])
