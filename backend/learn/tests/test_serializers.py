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


class ChunkSerializerTestCase(TestCase):
    def test_chunk_serialization(self):
        chunk = Chunk.objects.create(name='wormholes', order=5, setting={'toolbox': 'fly'})
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {
            'id': chunk.pk,
            'name': 'wormholes',
            'order': 5,
            'setting': {'toolbox': 'fly'},
            'tasks': []}

    def test_serialize_chunk_with_default_setting(self):
        chunk = Chunk.objects.create(name='wormholes', order=5)
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {
            'id': chunk.pk,
            'name': 'wormholes',
            'order': 5,
            'setting': {},
            'tasks': []}

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
            'tasks': ['t1', 't2']}

    def test_serialize_multiple_chunks(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        chunks = Chunk.objects.filter(name__in=['c1', 'c2'])
        serializer = ChunkSerializer(chunks, many=True)
        assert serializer.data == [
            {'id': chunk1.pk, 'name': 'c1', 'order': 1, 'setting': {}, 'tasks': []},
            {'id': chunk2.pk, 'name': 'c2', 'order': 2, 'setting': {}, 'tasks': []}]

    def test_deserialize_new_chunk(self):
        data = {
            'name': 'wormholes',
            'order': 5,
            'setting': {'toolbox': 'fly'},
            'tasks': []}
        serializer = ChunkSerializer(data=data)
        assert serializer.is_valid()
        chunk = serializer.save()
        assert chunk.id is not None
        assert chunk.name == 'wormholes'
        assert chunk.order == 5
        assert chunk.setting == {'toolbox': 'fly'}
        assert chunk.tasks.count() == 0

    def test_deserialize_new_chunk_with_tasks(self):
        task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
        data = {
            'name': 'wormholes',
            'order': 5,
            'setting': {'toolbox': 'fly'},
            'tasks': ['t1']}
        serializer = ChunkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        chunk = serializer.save()
        assert list(chunk.tasks.all()) == [task1]


class MissionSerializerTestCase(TestCase):
    def test_serialize_mission_with_phases(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        chunk3 = Chunk.objects.create(name='c3', order=3)
        chunk1.subchunks.set([chunk2, chunk3])
        mission = Mission.objects.create(name='loops', chunk=chunk1, order=1)
        serializer = MissionSerializer(mission)
        assert serializer.data == {
            'id': mission.pk,
            'order': 1,
            'name': 'loops',
            'chunk_name': 'c1',
            'setting': {},
            'phases': [
                {'id': chunk2.pk, 'name': 'c2', 'order': 2, 'setting': {}, 'tasks': []},
                {'id': chunk3.pk, 'name': 'c3', 'order': 3, 'setting': {}, 'tasks': []}]}

    def test_serialize_mission_with_settings(self):
        chunk = Chunk.objects.create(name='c1', order=1, setting={'toolbox': 'fly'})
        mission = Mission.objects.create(name='m1', chunk=chunk, order=1)
        serializer = MissionSerializer(mission)
        assert serializer.data == {
            'id': mission.pk,
            'order': 1,
            'name': 'm1',
            'chunk_name': 'c1',
            'setting': {'toolbox': 'fly'},
            'phases': []}
