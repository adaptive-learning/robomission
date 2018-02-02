from django.test import TestCase
from learn.models import Chunk, Mission
from learn.serializers import ChunkSerializer, MissionSerializer


class ChunkSerializerTestCase(TestCase):
    def test_chunk_serialization(self):
        chunk = Chunk.objects.create(name='wormholes', order=5)
        serializer = ChunkSerializer(chunk)
        assert serializer.data == {'id': chunk.pk, 'name': 'wormholes', 'order': 5}

    def test_multiple_chunks_serialization(self):
        chunk1 = Chunk.objects.create(name='c1', order=1)
        chunk2 = Chunk.objects.create(name='c2', order=2)
        chunks = Chunk.objects.filter(name__in=['c1', 'c2'])
        serializer = ChunkSerializer(chunks, many=True)
        assert serializer.data == [
            {'id': chunk1.pk, 'name': 'c1', 'order': 1},
            {'id': chunk2.pk, 'name': 'c2', 'order': 2}]


class MissionSerializerTestCase(TestCase):
    def test_mission_serialization(self):
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
            'phases': [
                {'id': chunk2.pk, 'name': 'c2', 'order': 2},
                {'id': chunk3.pk, 'name': 'c3', 'order': 3}]}
