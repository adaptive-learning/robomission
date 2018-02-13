from django.test import TestCase
from learn.models import Chunk, Mission, Task
from learn.serializers import SettingSerializer, ChunkSerializer, MissionSerializer


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


class ChunkSerializerTestCase(TestCase):
    def test_chunk_serialization(self):
        chunk = Chunk.objects.create(name='wormholes', order=5, setting={'toolbox': 'fly'})
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {
            'id': chunk.pk,
            'name': 'wormholes',
            'order': 5,
            'setting': {'toolbox': 'fly'},
            'tasks': [],
            'subchunks': []}

    def test_serialize_chunk_with_default_setting(self):
        chunk = Chunk.objects.create(name='wormholes', order=5)
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {
            'id': chunk.pk,
            'name': 'wormholes',
            'order': 5,
            'setting': {},
            'tasks': [],
            'subchunks': []}

    def test_serialize_chunk_with_tasks(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        task2 = Task.objects.create(id=2, name='t2', setting='{}', solution='')
        chunk = Chunk.objects.create(name='wormholes', order=5)
        chunk.tasks.set([task1, task2])
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {
            'id': chunk.pk,
            'name': 'wormholes',
            'order': 5,
            'setting': {},
            'tasks': ['t1', 't2'],
            'subchunks': []}

    def test_serialize_chunk_with_subchunks(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        task2 = Task.objects.create(id=2, name='t2', setting='{}', solution='')
        chunk1 = Chunk.objects.create(name='c1', order=5)
        chunk2 = Chunk.objects.create(name='c2', order=6)
        chunk1.tasks.set([task1])
        chunk1.subchunks.set([chunk2])
        chunk2.tasks.set([task2])
        serializer = ChunkSerializer(chunk1)
        assert serializer.data == {
            'id': chunk1.pk,
            'name': 'c1',
            'order': 5,
            'setting': {},
            'tasks': ['t1'],
            'subchunks': ['c2']}

    def test_serialize_multiple_chunks(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        chunks = Chunk.objects.filter(name__in=['c1', 'c2'])
        serializer = ChunkSerializer(chunks, many=True)
        assert serializer.data == [
            {'id': chunk1.pk, 'name': 'c1', 'order': 1, 'setting': {},
             'tasks': [], 'subchunks': []},
            {'id': chunk2.pk, 'name': 'c2', 'order': 2, 'setting': {},
             'tasks': [], 'subchunks': []}]

    def test_deserialize_new_chunk(self):
        data = {
            'id': 1,
            'name': 'wormholes',
            'setting': {'toolbox': 'fly'}}
        serializer = ChunkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save(order=5)
        assert chunk.id is not None
        assert chunk.name == 'wormholes'
        assert chunk.order == 5
        assert chunk.setting == {'toolbox': 'fly'}
        assert chunk.tasks.count() == 0
        assert chunk.subchunks.count() == 0

    def test_deserialize_chunk_without_setting(self):
        data = {
            'id': 1,
            'name': 'wormholes',
            'tasks': []}
        serializer = ChunkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save(order=5)
        assert chunk.setting == {}

    def test_deserialize_new_chunk_with_tasks(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        data = {
            'id': 1,
            'name': 'wormholes',
            'setting': {'toolbox': 'fly'},
            'tasks': ['t1']}
        serializer = ChunkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save(order=5)
        assert list(chunk.tasks.all()) == [task1]

    def test_update_existing_chunk(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        chunk = Chunk.objects.create(id=1, name='c1', order=1)
        data = {
            'id': 1,
            'name': 'c2',
            'setting': {'toolbox': 'fly'},
            'tasks': ['t1']}
        serializer = ChunkSerializer(chunk, data=data)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save(order=5)
        chunk_db = Chunk.objects.get(pk=1)
        assert chunk == chunk_db
        assert chunk_db.name == 'c2'
        assert chunk_db.order == 5
        assert chunk_db.setting == {'toolbox': 'fly'}
        assert list(chunk_db.tasks.all()) == [task1]

    def test_change_tasks_of_existing_chunk(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        task2 = Task.objects.create(id=2, name='t2', setting='{}', solution='')
        task3 = Task.objects.create(id=3, name='t3', setting='{}', solution='')
        chunk = Chunk.objects.create(id=1, name='c1', order=1)
        chunk.tasks.add(task1, task2)
        data = {
            'name': 'c1',
            'tasks': ['t2', 't3']}
        serializer = ChunkSerializer(chunk, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save()
        chunk_db = Chunk.objects.get(pk=1)
        assert chunk == chunk_db
        assert set(chunk_db.tasks.all()) == {task2, task3}

    def test_change_subchunks_of_existing_chunk(self):
        chunk1 = Chunk.objects.create(id=1, name='c1', order=1)
        chunk2 = Chunk.objects.create(id=2, name='c2', order=2)
        chunk3 = Chunk.objects.create(id=3, name='c3', order=3)
        chunk4 = Chunk.objects.create(id=4, name='c4', order=4)
        chunk1.subchunks.add(chunk2, chunk3)
        data = {
            'name': 'c1',
            'subchunks': ['c3', 'c4']}
        serializer = ChunkSerializer(chunk1, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save()
        chunk_db = Chunk.objects.get(pk=1)
        assert chunk == chunk_db
        assert set(chunk_db.subchunks.all()) == {chunk3, chunk4}

    def test_deserialize_list_of_new_chunks(self):
        data = [{'id': 1, 'name': 'c1'}, {'id': 2, 'name': 'c2'}]
        serializer = ChunkSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        chunk1 = Chunk.objects.get(pk=1)
        chunk2 = Chunk.objects.get(pk=2)
        assert chunk1.name == 'c1'
        assert chunk1.order == 0
        assert chunk2.name == 'c2'
        assert chunk2.order == 1

    def test_deserialize_list_of_new_chunks__update_existing(self):
        Chunk.objects.create(id=2, name='c2', order=5)
        data = [{'id': 1, 'name': 'c1'}, {'id': 2, 'name': 'c2n'}]
        serializer = ChunkSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        chunk = Chunk.objects.get(pk=2)
        assert chunk.name == 'c2n'
        assert chunk.order == 1

    def test_deserialize_list_of_new_chunks__remove_old(self):
        Chunk.objects.create(id=2, name='c2')
        data = [{'id': 1, 'name': 'c1'}]
        serializer = ChunkSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert {chunk.pk for chunk in  Chunk.objects.all()} == {1}


class MissionSerializerTestCase(TestCase):
    def test_serialize_mission_with_phases(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        mission = Mission.objects.create(name='loops', chunk=chunk1, order=5)
        serializer = MissionSerializer(mission)
        assert serializer.data == {
            'id': mission.pk,
            'order': 5,
            'name': 'loops',
            'chunk': 'c1'}

    def test_deserialize_new_mission(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        data = {
            "id": 1,
            "name": "m1",
            "chunk": "c1"}
        serializer = MissionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        mission = serializer.save(order=2)
        assert mission.id == 1
        assert mission.name == 'm1'
        assert mission.order == 2
        assert mission.chunk == chunk1

    def test_update_existing_mission(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        mission = Mission.objects.create(id=1, name='m1', chunk=chunk1)
        data = {
            "id": 1,
            "name": "m1n",
            "chunk": "c2"}
        serializer = MissionSerializer(mission, data=data)
        serializer.is_valid(raise_exception=True)
        mission = serializer.save(order=5)
        mission_db = Mission.objects.get(pk=1)
        assert mission == mission_db
        assert mission.name == 'm1n'
        assert mission.order == 5
        assert mission.chunk == chunk2

    def test_deserialize_list_of_new_missions(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        data = [
            {'id': 1, 'name': 'm1', 'chunk': 'c1'},
            {'id': 2, 'name': 'm2', 'chunk': 'c2'}]
        serializer = MissionSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        missions = list(Mission.objects.all())
        assert len(missions) == 2
        assert missions[0].name == 'm1'
        assert missions[0].order == 1
        assert missions[0].chunk == chunk1
        assert missions[1].name == 'm2'
        assert missions[1].order == 2
        assert missions[1].chunk == chunk2

    def test_deserialize_list_of_new_missions__update_existing(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        Mission.objects.create(id=1, name='m1', chunk=chunk1)
        data = [{'id': 1, 'name': 'm1n', 'chunk': 'c2'}]
        serializer = MissionSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        missions = list(Mission.objects.all())
        assert len(missions) == 1
        assert missions[0].id == 1
        assert missions[0].name == 'm1n'
        assert missions[0].order == 1
        assert missions[0].chunk == chunk2

    def test_deserialize_list_of_new_missions__delete_existing(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        Mission.objects.create(id=1, name='m1', chunk=chunk1)
        data = [{'id': 2, 'name': 'm2', 'chunk': 'c2'}]
        serializer = MissionSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        missions = list(Mission.objects.all())
        assert len(missions) == 1
        assert missions[0].id == 2
        assert missions[0].name == 'm2'
        assert missions[0].order == 1
        assert missions[0].chunk == chunk2
